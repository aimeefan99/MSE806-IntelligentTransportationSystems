ObjC.import("Foundation");
ObjC.import("PDFKit");

const args = $.NSProcessInfo.processInfo.arguments.js.slice(4);
if (args.length < 1 || args.length > 3) {
  throw new Error("usage: osascript -l JavaScript extract_pdf.js <path> [start-page] [end-page]");
}

const path = ObjC.unwrap(args[0]);
const url = $.NSURL.fileURLWithPath(path);
const document = $.PDFDocument.alloc.initWithURL(url);
if (!document) {
  throw new Error("could not open PDF");
}

const start = args.length >= 2 ? Math.max(1, Number(ObjC.unwrap(args[1]))) : 1;
const end = args.length >= 3 ? Math.min(Number(document.pageCount), Number(ObjC.unwrap(args[2]))) : Number(document.pageCount);
const chunks = [];
for (let index = start - 1; index < end; index += 1) {
  const page = document.pageAtIndex(index);
  const text = page && page.string ? ObjC.unwrap(page.string) : "";
  chunks.push(`===== PAGE ${index + 1} =====\n${text}`);
}
chunks.join("\n");
