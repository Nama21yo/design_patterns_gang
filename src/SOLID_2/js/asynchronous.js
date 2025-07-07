const numbers = [1, 2, 3, 4];

// Callback function
const double = (n) => n * 2;

// Higher-Order Function
const doubledNumbers = numbers.map(double);

console.log(doubledNumbers); // [2, 4, 6, 8]

// Callback function
const isEven = (n) => n % 2 === 0;

// Higher-Order Function
const evenNumbers = numbers.filter(isEven);

console.log(evenNumbers); // [2, 4]

// Callback function
const sum = (accumulator, current) => accumulator + current;

// Higher-Order Function
const total = numbers.reduce(sum, 0);

console.log(total); // 10

// Callback function for ascending
const ascending = (a, b) => a - b;

// Higher-Order Function
const sortedAsc = numbers.sort(ascending);

console.log(sortedAsc); // [1, 2, 3, 4, 5]

// Callback function for descending
const descending = (a, b) => b - a;

// Higher-Order Function
const sortedDesc = numbers.sort(descending);

console.log(sortedDesc); // [5, 4, 3, 2, 1]

function greet(name) {
  console.log("Hello, " + name);
}

function runCallback(callback) {
  const name = "Doku";
  // Inversion of Control: runCallback decides when to call your function
  callback(name);
}

runCallback(greet); // You pass 'greet', but 'runCallback' controls when it runs

console.log("Start");

// Async function using setTimeout
setTimeout(() => {
  console.log("Inside setTimeout (should run after 2s)");
}, 2000);

// Blocking loop
for (let i = 0; i < 1e9; i++) {
  // This does nothing but wastes time
}

console.log("End of loop");

const fetchData = new Promise(function (resolve, reject) {
  setTimeout(() => {
    const success = true; // change to false to test rejection
    if (success) {
      resolve("Data fetched successfully!");
    } else {
      reject("Failed to fetch data.");
    }
  }, 2000); // simulate a 2-second delay
});

// Use the promise
fetchData
  .then((data) => {
    console.log("Success:", data);
  })
  .catch((error) => {
    console.error("Error:", error);
  });

const delayedMessage = new Promise((res, rej) => {
  setTimeout(() => {
    const ok = true;
    ok ? res("All good!") : rej("Something went wrong.");
  }, 1000);
});

delayedMessage
  .then((msg) => console.log("✅", msg))
  .catch((err) => console.log("❌", err));

console.log("Start");

// Create a Promise with a long task
const bigTaskPromise = new Promise((resolve, reject) => {
  console.log("Inside Promise - starting long loop");

  for (let i = 0; i < 1e9; i++) {
    // time-consuming task
  }

  console.log("Loop done");

  resolve("Finished heavy computation");
});

bigTaskPromise.then((message) => {
  console.log("✅", message);
});

console.log("End");

console.log("Start");

const timeoutPromise = new Promise((resolve, reject) => {
  console.log("Inside Promise - setting timeout");
  setTimeout(() => {
    resolve("Done after 2 seconds");
  }, 2000);
});

timeoutPromise.then((message) => {
  console.log("✅", message);
});

console.log("End");

console.log("📚 Exam results are being checked...");

// Mock children's grades
const childGrades = {
  Alice: 90,
  Bob: 87,
};

// Father makes a promise
function promiseTripToFrance(grades) {
  return new Promise((resolve, reject) => {
    console.log("👨‍👧‍👦 Father is checking grades...");

    // Simulate checking delay
    setTimeout(() => {
      const alicePassed = grades.Alice >= 85;
      const bobPassed = grades.Bob >= 85;

      if (alicePassed && bobPassed) {
        resolve("🎉 Both kids passed! Trip to France is ON!");
      } else {
        reject("😢 One or both kids didn't meet the grade requirement. No trip.");
      }
    }, 2000);
  });
}

// Now we handle the promise with chaining
promiseTripToFrance(childGrades)
  .then((message) => {
    console.log("✅ SUCCESS:", message);
    // Promise chaining: book the flight
    return bookFlight();
  })
  .then((ticketInfo) => {
    console.log("✈️ Flight booked:", ticketInfo);
    // Next chained task: prepare passports
    return preparePassports();
  })
  .then((passportStatus) => {
    console.log("🛂 Passports ready:", passportStatus);
  })
  .catch((error) => {
    // Handle any failure in the chain
    console.error("❌ FAILURE:", error);
  })
  .finally(() => {
    console.log("👨‍👧‍👦 Father's promise handling is complete.");
  });

// Helper: Book flight (returns a Promise)
function bookFlight() {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve("✈️ Tickets booked to Paris with Air France.");
    }, 1500);
  });
}

// Helper: Prepare passports (returns a Promise)
function preparePassports() {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve("🛂 All passports are valid and packed!");
    }, 1000);
  });
}
// 📚 Exam results are being checked...
// 👨‍👧‍👦 Father is checking grades...
// ✅ SUCCESS: 🎉 Both kids passed! Trip to France is ON!
// ✈️ Flight booked: ✈️ Tickets booked to Paris with Air France.
// 🛂 Passports ready: 🛂 All passports are valid and packed!
// 👨‍👧‍👦 Father's promise handling is complete.


// Step 1: Fake download function
function downloadData(url) {
  return new Promise((resolve) => {
    console.log(`⬇️ Starting download from ${url}...`);
    setTimeout(() => {
      const data = "Fake data content from " + url;
      console.log("✅ Download complete.");
      resolve(data);
    }, 1500);
  });
}

// Step 2: Save data to file (simulate)
function saveToFile(data) {
  return new Promise((resolve) => {
    console.log("💾 Saving data to file...");
    setTimeout(() => {
      const filename = "data-file.txt";
      console.log(`📁 Data saved to ${filename}`);
      resolve(filename);
    }, 1000);
  });
}

// Step 3: Upload file to another URL
function uploadFile(filename, destinationUrl) {
  return new Promise((resolve) => {
    console.log(`📤 Uploading ${filename} to ${destinationUrl}...`);
    setTimeout(() => {
      console.log("✅ Upload complete.");
      resolve("Upload success");
    }, 1000);
  });
}

// Run the flow using .then() chaining
downloadData("https://fake-api.com/data")
  .then((data) => saveToFile(data))
  .then((filename) => uploadFile(filename, "https://fake-upload.com/target"))
  .then((result) => console.log("🎉 All steps completed:", result))
  .catch((err) => console.error("❌ Error:", err));


async function processDataFlow() {
  try {
    console.log("=== Starting Async Flow ===");

    const data = await downloadData("https://fake-api.com/data");
    const filename = await saveToFile(data);
    const uploadResult = await uploadFile(filename, "https://fake-upload.com/target");

    console.log("🎉 All steps completed:", uploadResult);
  } catch (err) {
    console.error("❌ Error during async process:", err);
  }
}

processDataFlow();
