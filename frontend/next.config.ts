/** @type {import('next').NextConfig} */
const nextConfig = {
  allowedDevOrigins: [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://192.168.29.243:3000",
    "http://192.168.29.243:3001",
  ],
};

module.exports = nextConfig;
