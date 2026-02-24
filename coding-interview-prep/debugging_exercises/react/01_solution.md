# Solution: Infinite Render Dashboard

## Bug 1 -- Infinite Re-render

**Location:** The `fetchOptions` object and the `useEffect` dependency array.

**What happens:**
- `fetchOptions` is a plain object literal defined in the component body.
- On every render, a **new object reference** is created (even if the values inside are identical).
- `useEffect` compares dependencies with `Object.is` (reference equality). A new object fails that check every time.
- The effect fires, calls `setProjects` / `setLastRefreshed`, which triggers a re-render, which creates a new `fetchOptions`, which fires the effect again -- infinite loop.

**Fix:** Replace the inline object with a `useMemo`, or depend on the **primitive values** directly instead of the object.

```jsx
// Option A: depend on the primitive value, not the object
useEffect(() => {
  let cancelled = false;
  setIsLoading(true);
  setError(null);

  fetchProjects(searchFilter)
    .then((data) => {
      if (!cancelled) {
        setProjects(data);
        setLastRefreshed(new Date());
        setIsLoading(false);
      }
    })
    .catch((err) => {
      if (!cancelled) {
        setError(err.message);
        setIsLoading(false);
      }
    });

  return () => { cancelled = true; };
}, [searchFilter]);  // <-- primitive string, stable between renders
```

```jsx
// Option B: memoize the options object
const fetchOptions = useMemo(
  () => ({ filter: searchFilter, includeArchived: true }),
  [searchFilter]
);
// ...then [fetchOptions] in the dependency array is safe
```

---

## Bug 2 -- Stale Closure in Refresh Handler

**Location:** `handleRefresh` is wrapped in `useCallback` with an **empty dependency array** `[]`.

**What happens:**
- The callback is created once on mount and never re-created.
- It closes over the initial value of `searchFilter`, which is `""`.
- No matter what the user types, clicking "Refresh" always calls `fetchProjects("")`, fetching all projects and appearing to ignore the filter.

**Fix:** Add `searchFilter` to the `useCallback` dependency array so the closure captures the current value.

```jsx
const handleRefresh = useCallback(() => {
  setIsLoading(true);
  setError(null);

  fetchProjects(searchFilter)
    .then((data) => {
      setProjects(data);
      setLastRefreshed(new Date());
      setIsLoading(false);
    })
    .catch((err) => {
      setError(err.message);
      setIsLoading(false);
    });
}, [searchFilter]);  // <-- include searchFilter
```

---

## Key Takeaways

- **Never put a non-memoized object/array in a `useEffect` dependency list.** React compares by reference, so a new literal on every render means the effect runs every render.
- **`useCallback` / `useMemo` dependency arrays must list every value from the enclosing scope that the function reads.** An empty `[]` freezes the closure at mount time; any state or props it references will be stale.
- The ESLint plugin `eslint-plugin-react-hooks` (`react-hooks/exhaustive-deps` rule) catches both of these automatically.
