abstract class AbstractParser {
  // Template method
  parse(file: string): void {
    this.openFile(file);
    this.parseData();
    this.closeFile();
  }

  protected openFile(file: string): void {
    console.log(`Opening file: ${file}`);
  }

  abstract parseData(): void; // Step to be implemented by subclasses

  protected closeFile(): void {
    console.log('Closing file');
  }
}

class CsvParser extends AbstractParser {
  parseData(): void {
    console.log('Parsing CSV data');
  }
}

class XmlParser extends AbstractParser {
  parseData(): void {
    console.log('Parsing XML data');
  }
}

class JsonParser extends AbstractParser {
  parseData(): void {
    console.log('Parsing JSON data');
  }
}

// Usage
const csvParser = new CsvParser();
csvParser.parse('data.csv');

const xmlParser = new XmlParser();
xmlParser.parse('data.xml');

const jsonParser = new JsonParser();
jsonParser.parse('data.json');
