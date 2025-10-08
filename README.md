# DocumentInteligence
🧠 Document Intelligence Framework (Lightweight & Private by Design)

This repository is the foundation for a fully-deployable Document Intelligence system, designed to run on consumer-grade machines with low latency and maximum data privacy. It supports intelligent querying and processing of a wide range of documents, including PDFs, scanned files, Excel sheets, CSVs, JSON, code files, and more.

Key Highlights:

✅ Custom lightweight models optimized for local CPU inference

🔐 Secure & private – all core processing runs locally; no data leaves the machine

📄 Supports scanned PDFs with built-in OCR and alignment (page-limit applies for free tier)

📊 Understands structure – tables, graphs, images, and sections are intelligently parsed

💬 Query any document using natural language prompts

🚀 Extensible architecture for tasks like code review, financial analysis, etc.

☁️ External models/services (only for advanced features) use encrypted payloads only

Ideal for building private, intelligent assistants for document-heavy workflows — fully offline by default, and cloud-augmented only when needed.

## PDF Deskewing (Auto Alignment)
> This module provides a fast and reliable way to detect and correct skewed pages in PDF files. It converts each page to an image, determines the skew angle, and deskews only the misaligned ones using OpenCV — preserving quality and improving OCR accuracy. Designed for internal use, with efficient multithreading and clean integration with pdf2image and deskew.
