import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  reactCompiler: true,
};

module.exports = {
  images: {
    domains: [
      'ik.imagekit.io',
      'res.cloudinary.com'
    ],
  },
}

export default nextConfig;

