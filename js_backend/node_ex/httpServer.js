const http = require("http");
// You create an HTTP server to:

// Serve web pages or APIs.

// Handle client requests like "give me data", "log me in", etc.

// Enable communication between the frontend (browser) and backend (your server logic).
// Using createServer we can creating a basic http server
// return server object and takes callback as an argument
const server = http.createServer(function listener() {
  // it is request listener
  // collect every http request that is being made by the client
});
// In basic computer networks any computer program that you execute is called Process
// If any external environment needs to communicate to process it needs a PORT
// Since on the same IP address multiple processes can run so we need PORT number not only IP address
//PORT
// logical connection that is used by programs and services to exchange information
// It specifically determines which program or service on a computer or server that is going to be used.
// Ports will have unique number that identifies them.
// it ranges from 0 - 65635
// Some common PORT are like 80, 443 - Web pages (https, https)
// 21 - FTP, 25 - Email
// It is always associated with IP address
// IP address is an identifier for computer or device on a network
// Ip addrss with Port work together to to exchange data  on a network
// Example 123.34.56.78:80 some i
//
