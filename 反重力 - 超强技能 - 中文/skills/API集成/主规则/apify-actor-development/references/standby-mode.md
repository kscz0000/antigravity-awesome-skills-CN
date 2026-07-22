# Actor 待机模式参考

## JavaScript 和 TypeScript

- **未经明确许可，永远不要在 `.actor/actor.json` 中禁用待机模式（`usesStandbyMode: false`）** - Actor 待机模式通过让 Actor 在后台准备就绪，等待传入的 HTTP 请求来解决这个问题。从某种意义上说，Actor 的行为就像实时 Web 服务器或标准 API 服务器，而不是运行一次逻辑来批量处理所有内容。除非有特定的文档化原因需要禁用，否则始终保持 `usesStandbyMode: true`
- **始终为待机 Actor 实现就绪探针处理器** - 在 GET / 端点处理 `x-apify-container-server-readiness-probe` 标头，以确保正确的 Actor 生命周期管理

您可以通过检查 `.actor/actor.json` 中的 `usesStandbyMode` 属性来识别待机 Actor。仅当此属性设置为 `true` 时才实现就绪探针。

### 就绪探针实现示例

```javascript
// Apify standby readiness probe at root path
app.get('/', (req, res) => {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    if (req.headers['x-apify-container-server-readiness-probe']) {
        res.end('Readiness probe OK\n');
    } else {
        res.end('Actor is ready\n');
    }
});
```

关键点：

- 检测传入请求中的 `x-apify-container-server-readiness-probe` 标头
- 对就绪探针和正常请求都响应 HTTP 200 状态码
- 这使得待机模式下能够正确管理 Actor 生命周期

## Python

- **未经明确许可，永远不要在 `.actor/actor.json` 中禁用待机模式（`usesStandbyMode: false`）** - Actor 待机模式通过让 Actor 在后台准备就绪，等待传入的 HTTP 请求来解决这个问题。从某种意义上说，Actor 的行为就像实时 Web 服务器或标准 API 服务器，而不是运行一次逻辑来批量处理所有内容。除非有特定的文档化原因需要禁用，否则始终保持 `usesStandbyMode: true`
- **始终为待机 Actor 实现就绪探针处理器** - 在 GET / 端点处理 `x-apify-container-server-readiness-probe` 标头，以确保正确的 Actor 生命周期管理

您可以通过检查 `.actor/actor.json` 中的 `usesStandbyMode` 属性来识别待机 Actor。仅当此属性设置为 `true` 时才实现就绪探针。

### 就绪探针实现示例

```python
# Apify standby readiness probe
from http.server import SimpleHTTPRequestHandler

class GetHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Handle Apify standby readiness probe
        if 'x-apify-container-server-readiness-probe' in self.headers:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Readiness probe OK')
            return

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Actor is ready')
```

关键点：

- 检测传入请求中的 `x-apify-container-server-readiness-probe` 标头
- 对就绪探针和正常请求都响应 HTTP 200 状态码
- 这使得待机模式下能够正确管理 Actor 生命周期
