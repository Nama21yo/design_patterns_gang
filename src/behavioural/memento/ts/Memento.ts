class EditorMemento {
  private readonly state: string; // for now the state is the content

  constructor(state: string) {
    this.state = state;
  }

  getContent(): string {
    return this.state;
  }
}
