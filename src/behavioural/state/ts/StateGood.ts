// State interface
interface DocumentState {
  publish(context: DocumentContext): void;
  moderate(context: DocumentContext): void;
}

// Concrete States
class DraftState implements DocumentState {
  publish(context: DocumentContext): void {
    console.log('Publishing document...');
    context.setState(new PublishedState());
  }
  moderate(context: DocumentContext): void {
    console.log('Document sent for moderation.');
    context.setState(new ModerationState());
  }
}

class PublishedState implements DocumentState {
  publish(context: DocumentContext): void {
    console.log('Document already published.');
  }
  moderate(context: DocumentContext): void {
    console.log('Published document cannot be moderated.');
  }
}

class ModerationState implements DocumentState {
  publish(context: DocumentContext): void {
    console.log('Cannot publish: Document in moderation.');
  }
  moderate(context: DocumentContext): void {
    console.log('Document already in moderation.');
  }
}

// Context class
class DocumentContext {
  private state: DocumentState;

  constructor() {
    this.state = new DraftState(); // initial state
  }

  setState(state: DocumentState): void {
    this.state = state;
  }

  publish(): void {
    this.state.publish(this);
  }

  moderate(): void {
    this.state.moderate(this);
  }
}

// Usage
const document = new DocumentContext();
document.publish();   // Publishing document...
document.moderate();  // Published document cannot be moderated.
document.publish();   // Document already published.
