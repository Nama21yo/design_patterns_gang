// Abstract product interfaces
interface Button {
  paint(): void;
}
interface ScrollBar {
  paint(): void;
}

// Concrete products for Windows
class WindowsButton implements Button {
  paint() {
    console.log("Windows Button");
  }
}
class WindowsScrollBar implements ScrollBar {
  paint() {
    console.log("Windows ScrollBar");
  }
}https://jalammar.github.io/illustrated-transformer/

// Concrete products for Mac
class MacButton implements Button {
  paint() {
    console.log("Mac Button");
  }
}
class MacScrollBar implements ScrollBar {
  paint() {
    console.log("Mac ScrollBar");
  }
}

// concrete product for linux
class LinuxScrollBar implements ScrollBar {
  paint(): void {
    console.log("Linus Scrollbar");
  }
}
class LinuxButton implements Button {
  paint(): void {
    console.log("Linux Button");
  }
}
// Abstract factory interface
interface GUIFactory {
  createButton(): Button;
  createScrollBar(): ScrollBar;
}

// Concrete factories
class WindowsFactory implements GUIFactory {
  createButton(): Button {
    return new WindowsButton();
  }
  createScrollBar(): ScrollBar {
    return new WindowsScrollBar();
  }
}
class MacFactory implements GUIFactory {
  createButton(): Button {
    return new MacButton();
  }
  createScrollBar(): ScrollBar {
    return new MacScrollBar();
  }
}

class LinuxFactory implements GUIFactory {
  createButton(): Button {
    return new LinuxButton();
  }
  createScrollBar(): ScrollBar {
    return new LinuxScrollBar();
  }
}
// Client code only talks to GUIFactory and its products
function renderUI(factory: GUIFactory) {
  const button = factory.createButton();
  const scrollBar = factory.createScrollBar();
  button.paint();
  scrollBar.paint();
}

renderUI(new WindowsFactory()); // Windows Button, Windows ScrollBar
renderUI(new MacFactory()); // Mac Button, Mac ScrollBar
renderUI(new LinuxFactory());
//
