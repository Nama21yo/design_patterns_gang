// // Button and ScrollBar interfaces
// interface Button { paint(): void; }
// interface ScrollBar { paint(): void; }

// // Concrete implementations
// class WindowsButton implements Button {
//   paint() { console.log("Windows Button"); }
// }
// class MacButton implements Button {
//   paint() { console.log("Mac Button"); }
// }
// class WindowsScrollBar implements ScrollBar {
//   paint() { console.log("Windows ScrollBar"); }
// }
// class MacScrollBar implements ScrollBar {
//   paint() { console.log("Mac ScrollBar"); }
// }

// // Client code: direct instantiation
// function renderUI(os: string) {
//   let button: Button;
//   let scrollBar: ScrollBar;

//   if (os === "windows") {
//     button = new WindowsButton();
//     scrollBar = new WindowsScrollBar();
//   } else if (os === "mac") {
//     button = new MacButton();
//     scrollBar = new MacScrollBar();
//   }

//   button.paint();
//   scrollBar.paint();
// }

// renderUI("windows"); // Windows Button, Windows ScrollBar
// renderUI("mac");     // Mac Button, Mac ScrollBar
