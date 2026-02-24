// DEBUGGING EXERCISE: Find and fix the bug(s) in this implementation
//
// System: In-Memory Message Queue
// Description: A publish/subscribe message queue that supports multiple topics
// and multiple subscribers per topic. Publishers send messages to a topic,
// and all subscribers to that topic receive the message.
//
// Expected behavior:
//   - Subscribe() creates a subscription channel for a topic
//   - Publish() sends a message to all subscribers of a topic
//   - Unsubscribe() removes a subscriber and cleans up resources
//   - Publishing should not block the publisher, even if a subscriber is slow
//   - After Unsubscribe(), the subscriber's channel is closed so range loops exit
//
// Symptoms of the bug:
//   - Publishing to a topic with a slow subscriber causes the publisher to hang forever
//   - The entire Publish() call blocks, preventing other subscribers from receiving
//   - After Unsubscribe(), goroutines that were reading from the channel leak
//     (they block forever on a channel that is never closed)
//   - Tests timeout or deadlock
//
// Hint: Think about what happens when a subscriber's buffered channel is full.
//       Also check what Unsubscribe() does (and doesn't do) to the channel.

package msgqueue

import (
	"sync"
)

// Message represents a message in the queue.
type Message struct {
	Topic   string
	Payload interface{}
}

// Broker manages topics and their subscribers.
type Broker struct {
	mu          sync.RWMutex
	subscribers map[string]map[int]chan Message
	nextID      int
}

// NewBroker creates a new message broker.
func NewBroker() *Broker {
	return &Broker{
		subscribers: make(map[string]map[int]chan Message),
	}
}

// Subscribe creates a new subscription for the given topic.
// Returns a subscriber ID and a channel to receive messages.
func (b *Broker) Subscribe(topic string, bufferSize int) (int, <-chan Message) {
	b.mu.Lock()
	defer b.mu.Unlock()

	if _, ok := b.subscribers[topic]; !ok {
		b.subscribers[topic] = make(map[int]chan Message)
	}

	id := b.nextID
	b.nextID++

	ch := make(chan Message, bufferSize)
	b.subscribers[topic][id] = ch

	return id, ch
}

// Publish sends a message to all subscribers of the given topic.
func (b *Broker) Publish(topic string, payload interface{}) {
	b.mu.RLock()
	defer b.mu.RUnlock()

	subs, ok := b.subscribers[topic]
	if !ok {
		return
	}

	msg := Message{Topic: topic, Payload: payload}

	for _, ch := range subs {
		ch <- msg
	}
}

// Unsubscribe removes a subscriber from a topic.
func (b *Broker) Unsubscribe(topic string, id int) {
	b.mu.Lock()
	defer b.mu.Unlock()

	subs, ok := b.subscribers[topic]
	if !ok {
		return
	}

	delete(subs, id)

	if len(subs) == 0 {
		delete(b.subscribers, topic)
	}
}

// TopicSubscriberCount returns the number of subscribers for a topic.
func (b *Broker) TopicSubscriberCount(topic string) int {
	b.mu.RLock()
	defer b.mu.RUnlock()
	return len(b.subscribers[topic])
}
