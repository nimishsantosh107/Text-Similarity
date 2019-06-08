//export GOOGLE_APPLICATION_CREDENTIALS="/Users/nimish/Desktop/Angel/APP/credentials.json"

const vision = require('@google-cloud/vision');

// Creates a client
const client = new vision.ImageAnnotatorClient();

/**
 * TODO(developer): Uncomment the following line before running the sample.
 */
const fileName = 'https://previews.123rf.com/images/annasea/annasea1705/annasea170500670/78914875-life-is-beautiful-handwritten-black-text-on-white-background-vector-each-word-is-on-different-layers.jpg';

// Read a local image as a text document
const main = async ()=>{
  const [result] = await client.documentTextDetection(fileName);
  const fullTextAnnotation = result.fullTextAnnotation;
  console.log(`Full text: ${fullTextAnnotation.text}`);
}

main()