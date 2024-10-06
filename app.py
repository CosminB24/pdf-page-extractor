from flask import Flask, render_template, request, send_file
import os
import PyPDF2
import tempfile

app = Flask(__name__)

UPLOAD_FOLDER = tempfile.gettempdir()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def extract_pages(input_path, output_path, pages):
    with open(input_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()

        for page_num in pages:
            if 1 <= page_num <= len(reader.pages):
                writer.add_page(reader.pages[page_num - 1])

        with open(output_path, 'wb') as output_file:
            writer.write(output_file)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error="No file part")

        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error="No selected file")

        if file and file.filename.lower().endswith('.pdf'):
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(input_path)

            pages_input = request.form['pages']
            try:
                pages = [int(page.strip()) for page in pages_input.split(',')]
            except ValueError:
                return render_template('index.html', error="Invalid page numbers")

            if not pages:
                return render_template('index.html', error="No valid page numbers entered")

            output_filename = f"extracted_{file.filename}"
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

            try:
                extract_pages(input_path, output_path, pages)
                return send_file(output_path, as_attachment=True)
            except Exception as e:
                return render_template('index.html', error=f"An error occurred: {str(e)}")
        else:
            return render_template('index.html', error="Invalid file type. Please upload a PDF.")

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)