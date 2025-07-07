
//! Frame work vs Library
// there are farmers who give us raw materials, you may also go to baltena rather than grinding your spicies
// you may also go to restaurant eat with out doing
// most of the time we bring the recipes and cook the food
// This functionality is called library.
// Example: Reactjs, Better-Auth >> vary specific purpose just like farmer that give specific thing
// Express js doesn't have it is own ORM, doesn't resolve sockets it is kind of library
//? The collection of libraries is called FrameWork
// Example: Using other Library give SSR Nextjs, Nestjs

// Globals
console.log(process);
// process.stdout.write("hi")
console.log(__dirname);
// REPL Console -> Read, Execute, Print, Loop
// use node -> but in this case you won't acess __dirname
console.log(module);
// Module pattern of Programming
// Sorting.js
// there is index.js and want to use sorting
// so do require(__dirname + "/searching.js")
// If you want module.exports
// module is an object
// module.exports = {somefunction} or module.export = someFunction
// CommonJS and ES6
// for ES6 you can use Sorting.mjs

// The concept of Closure
// The concept of package
// A folder that contains package.json
// search on the documentation
// type : "module"
// ES6 -> named and deafult export

// #!/usr/bin/env node
// then use chmod 777 script.js
// ./script.js it works
// ./script.js Natnael Nexus
// How to consume
// console.loog(process.argv)
// console.log(process.argv[2].split("=")[2])

// let's talk about shebang / Hashbang
// To run a **C++ file like `./filename`**, you need to compile it into an executable using `g++`, then give it execute permission.

// But note: **C++ does *not* use a shebang** — it is a compiled language, not a script language like Node.js or Python.

// ---

// ### ✅ Step-by-step Example

// 1. Create a file `hello.cpp` with this content:

// ```cpp
// #include <iostream>

// int main() {
//     std::cout << "Hello from C++!" << std::endl;
//     return 0;
// }
// ```

// 2. Compile it:

// ```bash
// g++ hello.cpp -o hello
// ```

// This creates an executable named `hello`.

// 3. Make it executable (optional — most compilers set it already):

// ```bash
// chmod +x hello
// ```

// 4. Run it:

// ```bash
// ./hello
// ```

// You’ll see:

// ```
// Hello from C++!
// ```

// ---

// * write your `.cpp` file,
// * compile it using `g++`,
// * then run the compiled binary.

// Package Manager -> handles dependencies of package and it's dependencies
// show example with Expressjs
// they manage installation, dependency resolution
// so there is bun, npm and yarn
// npx -> to execute npm packages

//! Streams
// stream of integer when you get -1 do median


// fs module
// const fs = require('fs').promises;

// async function readAndWrite() {
//   try {
//     // Write some text to a file
//     await fs.writeFile('example.txt', 'Hello, this is a test!');

//     console.log('File written successfully.');

//     // Read the content from the file
//     const data = await fs.readFile('example.txt', 'utf-8');

//     console.log('File content:', data);
//   } catch (error) {
//     console.error('Error:', error);
//   }
// }

// readAndWrite();

// const fs = require('fs').promises;

// async function readAndWriteHtml() {
//   try {
//     // Step 1: Read the existing index.html file
//     const existingContent = await fs.readFile('index.html', 'utf-8');
//     console.log('Read index.html successfully.');

//     // Optional: You can process existingContent here if needed
//     // For now, we'll ignore it and write a new file

//     // Step 2: Prepare custom title and body
//     const title = 'My Custom Page Title';
//     const body = '<h1>Welcome to my custom page!</h1><p>This is dynamically generated.</p>';

//     // Step 3: Create the new HTML content with template strings
//     const newHtml = `<!DOCTYPE html>
// <html lang="en">
// <head>
//   <meta charset="UTF-8" />
//   <meta http-equiv="X-UA-Compatible" content="IE=edge" />
//   <meta name="viewport" content="width=device-width, initial-scale=1.0" />
//   <title>${title}</title>
// </head>
// <body>
//   ${body}
// </body>
// </html>`;

//     // Step 4: Write the new content to a new file, e.g. output.html
//     await fs.writeFile('output.html', newHtml, 'utf-8');
//     console.log('Written output.html successfully.');
//   } catch (err) {
//     console.error('Error:', err);
//   }
// }

// readAndWriteHtml();



// there is many libraries is too many high
//! Intoduction to Node

// you play with a lot of databases
// Implementing Backend APIs
// Business Logic
// Scalability and Maintenance

// ! Introduction to API
// Explain the I part which is Interface
// show fakeStore API
// show Swagger API doc

//! Representational State Transfer
// recommendation to follow that will help a lot of people
// set of guidelines(recommendation) that drive architecture of the web
// REST API: any api that follows recommendation of the REST API
// - prefers a client-server communication should happen over http/https
// - prefers JSON as the format to send and return data
// - How to make URLs?
// - In REST the main source of info is considered as a Resource
// Example- In Twitter, Tweet User Likes is a resources
// - There is also what we call actions
// Example - Creating User, Deleting Users
// The endpoints should use nouns(specifically plural nouns) not verbs
// medium.com/blogs , medium.com/blogs/2 -> The action isn't mention in the URL
// medium.com/createBlog -> not recommended
// - Every REST endpoint should be defend along with an HTTP method
// GET, POST, PATCH, PUT, DELETE (CRUD API)
// /blogs and method -> GET : retrieve data of all blogs
// /blogs/12 and method -> GET: retrieve data of blog with unique identifier vale is 12
// we use nesting for realtionships
// Example: /blogs/13/comments GET
// REST expects the response to have HTTP Status COdes
// API Versioning is recommended in REST
//  the process of managing and tracking changes to an API,
// what if the newer version being used explain the roll out concept
// slowly and steadly migrating to the newer version
// Sending data
// - Using Request Body
// - URL Params Exmaple: /blogs/:id
// - query params Example: /blogs?category=electronics&company=apple
//
