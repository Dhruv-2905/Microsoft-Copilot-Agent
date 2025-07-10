FROM node:18-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json /app/

# Install dependencies
RUN npm i

# Copy the entire project to the working directory
COPY . /app/

# Build the app for production
# RUN npm run build

# Expose port 3000
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
