class CsvParser {
  parse(file: string): void {
    console.log("Opening CSV file:", file);
    // CSV-specific parsing logic...
    console.log("Parsing CSV data...");
    console.log("Closing CSV file");
  }
}

class XmlParser {
  parse(file: string): void {
    console.log("Opening XML file:", file);
    // XML-specific parsing logic...
    console.log("Parsing XML data...");
    console.log("Closing XML file");
  }
}

class JsonParser {
  parse(file: string): void {
    console.log("Opening JSON file:", file);
    // JSON-specific parsing logic...
    console.log("Parsing JSON data...");
    console.log("Closing JSON file");
  }
}

// Usage
const csvParser = new CsvParser();
csvParser.parse("data.csv");

const xmlParser = new XmlParser();
xmlParser.parse("data.xml");

const jsonParser = new JsonParser();
jsonParser.parse("data.json");
