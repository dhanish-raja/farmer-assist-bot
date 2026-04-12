# 🌱 Agricultural Multimodal AI Chatbot

An end-to-end AI system that supports **multimodal agricultural queries** (text, speech, images, documents) and routes them to specialized deep learning models to generate intelligent responses.

---

## 🚀 Features

* 🌿 Plant Disease Detection
* 🐛 Pest Classification
* 🌍 Soil Classification
* 🌾 Crop Identification
* 🌱 Weed Detection
* 🔀 Intelligent Routing Model
* 🧠 NLP-based Query Understanding
* 🌐 Multilingual Support
* 🎤 Speech-to-Text & Text-to-Speech
* 📄 OCR for Documents
* 🔎 Hybrid Response System (Rule-based + RAG + Web Search)

---

## 🏗️ Architecture

```
User Input (Text / Speech / Image / Video / Document)
        ↓
Routing Model (Modality Detection)
        ↓
Task-specific Models
   ├── Plant Disease Model
   ├── Pest Model
   ├── Soil Model
   ├── Crop Model
   ├── Weed Model
   ├── OCR + NLP
        ↓
Response Engine
        ↓
Text / Voice Output
```

---

## 🧠 Models Summary

### 🐛 Pest Classification

* Dataset: Pestopia Tier-1
* Model: Custom CNN (ResNet-style)
* Classes: 21
* Accuracy: **70.35%**
* Loss: 0.9687

---

### 🌍 Soil Classification

* Dataset: Custom Soil Dataset
* Model: Ensemble (EfficientNetV2-L + ViT-L/16)
* Train Acc: 97.92%
* Val Acc: 95.02%
* Test Acc: **95.95%**
* Framework: PyTorch

---

### 🌱 Weed Detection

* Dataset: DeepWeeds
* Model: ResNet50 (Fine-tuned)
* Classes: 9
* Train Acc: **99.97%**
* Val Acc: **87.83%**

---

### 🌾 Crop Identification

* Dataset: Agricultural Crops Dataset
* Model: ResNet50
* Classes: 30
* Train Acc: **100%**
* Val Acc: ~74%

---

### 🔀 Routing Model (Core System)

* Dataset: Custom multimodal routing dataset
* Model: EfficientNetB0
* Classes: 6 (modalities/tasks)
* Train Accuracy: **99.29%**
* Validation Accuracy: **98.14%**
* Loss: 0.0221
* Role: Automatically routes user input to correct model

---

## 🖥️ Tech Stack

**Frontend**

* HTML, CSS, JavaScript

**Backend**

* Python (Flask)

**AI/ML**

* TensorFlow / Keras
* PyTorch
* OpenCV
* NLP (NER, preprocessing)

**Tools**

* Google Colab (training)
* Google Drive (storage)

---


---

## ⚙️ Setup

### Clone

```
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### Backend

```
pip install -r requirements.txt
python server.py
```

### Frontend

Open `index.html` in browser

---

## 🔍 Workflow

1. User provides input
2. Routing model identifies input type
3. Input is sent to appropriate model
4. Prediction + NLP processing
5. Response generated
6. Output returned (text/voice)

---

## 📊 Performance

| Model               | Accuracy   |
| ------------------- | ---------- |
| Routing Model       | **98.14%** |
| Soil Classification | **95.95%** |
| Weed Detection      | 87.83%     |
| Crop Identification | ~74%       |
| Pest Classification | 70.35%     |

---

## ⚠️ Limitations

* Crop model shows overfitting
* Performance depends on image quality
* Real-time inference not optimized

---

---

