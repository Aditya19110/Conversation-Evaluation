# Build stage
FROM node:18-alpine as build

WORKDIR /app

# Copy package files
COPY src/ui/package*.json ./
RUN npm ci --only=production

# Copy source code
COPY src/ui/ ./

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy build files
COPY --from=build /app/build /usr/share/nginx/html

# Copy nginx configuration
COPY docker/nginx/nginx.conf /etc/nginx/nginx.conf

# Expose port
EXPOSE 3000

# Start nginx
CMD ["nginx", "-g", "daemon off;"]