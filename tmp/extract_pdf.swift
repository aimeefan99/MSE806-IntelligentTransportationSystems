import Foundation
import PDFKit

guard CommandLine.arguments.count == 2 else {
    fputs("usage: extract_pdf <path>\n", stderr)
    exit(2)
}

let url = URL(fileURLWithPath: CommandLine.arguments[1])
guard let document = PDFDocument(url: url) else {
    fputs("could not open PDF\n", stderr)
    exit(1)
}

for index in 0..<document.pageCount {
    print("===== PAGE \(index + 1) =====")
    print(document.page(at: index)?.string ?? "")
}
