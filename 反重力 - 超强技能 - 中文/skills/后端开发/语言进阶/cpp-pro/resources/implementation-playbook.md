# C++ 实现手册

**日期：** 2026年3月23日  
**作者：** champbreed  
---

## 1. RAII 与资源管理
始终将裸资源包装在管理对象中，确保作用域退出时自动清理。
```cpp
// Good: Scope-bound cleanup
void process() {
    auto data = std::make_unique<uint8_t[]>(1024);
    // memory is freed automatically
}
```
## 2. 智能指针所有权
- **unique_ptr**：用于独占所有权。
- **shared_ptr**：用于跨组件的共享所有权。
- **weak_ptr**：用于打破循环引用。

## 3. 并发安全
始终使用 RAII 风格的锁，如 `std::lock_guard` 或 `std::unique_lock`。
```cpp
void update() {
    std::lock_guard<std::mutex> lock(mutex_); // Released automatically
    // thread-safe logic
}
```
## 4. 移动语义与效率
利用移动构造函数和 `std::move` 避免昂贵的拷贝操作。
```cpp
void processData(std::vector<std::string>&& data) {
    auto internalData = std::move(data); // Transfers ownership, no copy
}
```
## 5. 现代 STL 算法
优先使用算法而非手动循环，以提升可读性和优化性能。

```cpp
void sortData(std::vector<int>& myVector) {
    // Use std::ranges (C++20) for cleaner, safer iteration
    std::ranges::sort(myVector);
}