# PostRaft - AI-Powered Poster Generation Platform


### **System Architecture:**
```
User Request → API → Enqueue Job → Redis Queue
                                        ↓
                                   RQ Worker
                                        ↓
                              Render Engine
                                        ↓
                                   Upload S3
                                        ↓
                                  Save to DB
                                        ↓
                                Return Result

User ← API ← Fetch Result ← DB
```                                        

### **Complete Flow:**
```
User selects template + products
          ↓
API validates & enqueues job
          ↓
Redis Queue holds job
          ↓
RQ Worker processes job
          ↓
Rendering Engine creates poster
          ↓
Upload to S3/cloudinary
          ↓
Save to database
          ↓
User polls job status
          ↓
Job completes → poster ready
          ↓
User downloads poster
```

### **Poster API Endpoints:**
```
POST   /api/posters/generate       - Queue generation
GET    /api/posters/job/:id        - Check job status
GET    /api/posters                - List posters
GET    /api/posters/:id            - Get poster
DELETE /api/posters/:id            - Delete poster
POST   /api/posters/download       - Download ZIP
GET    /api/posters/stats          - Usage statistics
```