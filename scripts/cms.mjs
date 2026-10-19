process.env.BIND_HOST = '127.0.0.1';
process.env.ORIGIN = 'http://localhost:4321';
await import('decap-server');
