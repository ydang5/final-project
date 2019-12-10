# Final Project Documentary

### API Endpoints




Base code sample for uploading sample csv
```bash
openssl base64 -in sample.csv > sample.csv.base64 \
http POST :8000/api/student-file-uploads attached_file_name=sample.csv attached_file=@sample.csv.base64 title="2018 Master sheet test" description="This is a test of uploading file."
```
