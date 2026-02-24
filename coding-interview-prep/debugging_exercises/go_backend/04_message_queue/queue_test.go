package msgqueue

import (
	"sync"
	"testing"
	"time"
)

func TestBasicPubSub(t *testing.T) {
	broker := NewBroker()
	_, ch := broker.Subscribe("events", 10)

	broker.Publish("events", "hello")

	select {
	case msg := <-ch:
		if msg.Payload != "hello" {
			t.Errorf("expected payload 'hello', got %v", msg.Payload)
		}
		if msg.Topic != "events" {
			t.Errorf("expected topic 'events', got %s", msg.Topic)
		}
	case <-time.After(time.Second):
		t.Fatal("timed out waiting for message")
	}
}

func TestMultipleSubscribers(t *testing.T) {
	broker := NewBroker()
	_, ch1 := broker.Subscribe("news", 10)
	_, ch2 := broker.Subscribe("news", 10)

	broker.Publish("news", "breaking")

	for i, ch := range []<-chan Message{ch1, ch2} {
		select {
		case msg := <-ch:
			if msg.Payload != "breaking" {
				t.Errorf("subscriber %d: expected 'breaking', got %v", i, msg.Payload)
			}
		case <-time.After(time.Second):
			t.Fatalf("subscriber %d: timed out waiting for message", i)
		}
	}
}

func TestPublishToNonexistentTopic(t *testing.T) {
	broker := NewBroker()
	// Should not panic or block
	broker.Publish("nonexistent", "hello")
}

func TestUnsubscribeStopsReceiving(t *testing.T) {
	broker := NewBroker()
	id, ch := broker.Subscribe("updates", 10)

	// Publish one message
	broker.Publish("updates", "first")
	select {
	case <-ch:
		// Good, received
	case <-time.After(time.Second):
		t.Fatal("timed out waiting for first message")
	}

	// Unsubscribe
	broker.Unsubscribe("updates", id)

	// After unsubscribe, the channel should be closed so that
	// a range loop or receive will not block forever.
	select {
	case _, ok := <-ch:
		if ok {
			t.Error("expected channel to be closed after unsubscribe")
		}
		// Channel was closed, this is correct behavior
	case <-time.After(2 * time.Second):
		t.Fatal("channel was not closed after Unsubscribe — goroutine would leak")
	}

	if broker.TopicSubscriberCount("updates") != 0 {
		t.Error("expected 0 subscribers after unsubscribe")
	}
}

func TestSlowSubscriberDoesNotBlockPublisher(t *testing.T) {
	broker := NewBroker()

	// Subscriber with a tiny buffer of 1
	_, slowCh := broker.Subscribe("data", 1)
	_, fastCh := broker.Subscribe("data", 100)

	// Fill up the slow subscriber's buffer
	broker.Publish("data", "msg-1")

	// Read from the fast subscriber to confirm it got the message
	select {
	case <-fastCh:
	case <-time.After(time.Second):
		t.Fatal("fast subscriber didn't get first message")
	}

	// Now the slow subscriber's buffer is full (has msg-1 sitting in it).
	// Publishing again should NOT block — it should either drop the message
	// for the slow subscriber or use a timeout.
	done := make(chan struct{})
	go func() {
		broker.Publish("data", "msg-2")
		close(done)
	}()

	select {
	case <-done:
		// Good — Publish returned without blocking
	case <-time.After(3 * time.Second):
		t.Fatal("Publish() blocked because a subscriber's buffer was full — " +
			"publisher should not block on slow subscribers")
	}

	// Fast subscriber should have received the second message too
	select {
	case msg := <-fastCh:
		if msg.Payload != "msg-2" {
			t.Errorf("fast subscriber expected 'msg-2', got %v", msg.Payload)
		}
	case <-time.After(time.Second):
		t.Fatal("fast subscriber didn't receive msg-2")
	}

	// Drain slow subscriber
	_ = <-slowCh
}

func TestConcurrentPublishSubscribe(t *testing.T) {
	broker := NewBroker()
	var wg sync.WaitGroup

	// Start subscribers
	channels := make([]<-chan Message, 5)
	for i := 0; i < 5; i++ {
		_, ch := broker.Subscribe("concurrent", 100)
		channels[i] = ch
	}

	// Concurrent publishers
	numPublishers := 5
	msgsPerPublisher := 10
	for i := 0; i < numPublishers; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			for j := 0; j < msgsPerPublisher; j++ {
				broker.Publish("concurrent", id*100+j)
			}
		}(i)
	}

	wg.Wait()

	totalExpected := numPublishers * msgsPerPublisher
	for i, ch := range channels {
		count := 0
		timeout := time.After(2 * time.Second)
	drain:
		for {
			select {
			case <-ch:
				count++
				if count == totalExpected {
					break drain
				}
			case <-timeout:
				break drain
			}
		}
		if count != totalExpected {
			t.Errorf("subscriber %d received %d messages, expected %d", i, count, totalExpected)
		}
	}
}

func TestUnsubscribeOneOfMany(t *testing.T) {
	broker := NewBroker()

	id1, ch1 := broker.Subscribe("multi", 10)
	_, ch2 := broker.Subscribe("multi", 10)

	// Unsubscribe first, second should still work
	broker.Unsubscribe("multi", id1)

	broker.Publish("multi", "after-unsub")

	// ch1 should be closed (no message, and should not block)
	select {
	case _, ok := <-ch1:
		if ok {
			t.Error("expected ch1 to be closed after unsubscribe")
		}
	case <-time.After(2 * time.Second):
		t.Fatal("ch1 not closed after unsubscribe")
	}

	// ch2 should receive the message
	select {
	case msg := <-ch2:
		if msg.Payload != "after-unsub" {
			t.Errorf("ch2 expected 'after-unsub', got %v", msg.Payload)
		}
	case <-time.After(time.Second):
		t.Fatal("ch2 timed out waiting for message")
	}
}
