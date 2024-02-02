const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/latest',
    createProxyMiddleware({
      target: 'http://api:8888',
      changeOrigin: true,
    })
  );
};