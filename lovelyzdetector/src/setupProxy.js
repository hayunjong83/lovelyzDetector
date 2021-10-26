const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = (app) => {
    app.use(
        "/lovelyz",
        createProxyMiddleware({
            target: "http://localhost:5000",
            changeOrigin: true
        })
    );
};