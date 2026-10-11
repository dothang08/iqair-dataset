# 🌍 Air Quality Analysis & Prediction

> Thu thập, phân tích và dự báo chất lượng không khí tại một số thành phố ở Việt Nam bằng Python, Machine Learning và GitHub Actions.

## 📌 Giới thiệu

Ô nhiễm không khí đang là một vấn đề đáng quan tâm tại nhiều đô thị lớn ở Việt Nam. Tuy nhiên, dữ liệu phục vụ cho việc theo dõi, phân tích và nghiên cứu chất lượng không khí thường phân tán và khó khai thác một cách có hệ thống.

Dự án này được xây dựng nhằm tạo ra một quy trình hoàn chỉnh gồm:

- Tự động thu thập dữ liệu chất lượng không khí từ IQAir.
- Lưu trữ và cập nhật dữ liệu định kỳ.
- Phân tích xu hướng và mối tương quan giữa các yếu tố môi trường.
- Xây dựng mô hình Machine Learning để dự báo chỉ số AQI.

Dự án được phát triển theo hướng vừa phục vụ mục đích nghiên cứu, vừa là một bài toán thực tế để thực hành Python, Data Analysis và Machine Learning.

---

## ✨ Chức năng chính

- 🤖 Tự động thu thập dữ liệu mỗi giờ bằng GitHub Actions.
- 🐍 Crawl và xử lý dữ liệu bằng Python.
- 📊 Phân tích dữ liệu chất lượng không khí bằng Jupyter Notebook.
- 🧹 Làm sạch và tiền xử lý dữ liệu.
- 📈 Trực quan hóa xu hướng AQI theo thời gian và khu vực.
- 🔍 Phân tích mối tương quan giữa AQI và các yếu tố môi trường.
- 🧠 Xây dựng mô hình dự báo AQI bằng Machine Learning / Deep Learning.
- 🌲 Thử nghiệm Random Forest Regressor.
- 🔁 Thử nghiệm mô hình LSTM cho dữ liệu chuỗi thời gian.
- 📏 Đánh giá mô hình bằng các chỉ số MAE, MSE, RMSE và R².

---

## 🛠 Công nghệ sử dụng

### Ngôn ngữ và thư viện
- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- TensorFlow / Keras
- Jupyter Notebook

### Công cụ
- Git
- GitHub
- GitHub Actions
- CSV

---

## 🔄 Quy trình hoạt động

```text
IQAir
  │
  ▼
Python Crawler
  │
  ▼
CSV Dataset
  │
  ├──► Data Cleaning & Preprocessing
  │
  ├──► Exploratory Data Analysis
  │
  └──► Machine Learning
          │
          ├── Random Forest
          └── LSTM
                │
                ▼
          AQI Prediction
```

Quy trình thu thập dữ liệu được tự động hóa bằng GitHub Actions và chạy định kỳ mỗi giờ.

---

## 📂 Cấu trúc dự án

```text
iqair-dataset/
│
├── .github/
│   └── workflows/
│       └── ...                  # GitHub Actions tự động thu thập dữ liệu
│
├── result/                      # Dữ liệu AQI theo từng thành phố/thời gian
│   ├── ha-noi/
│   ├── da-nang/
│   └── ho-chi-minh/
│
├── Phan_tich.ipynb              # Phân tích và trực quan hóa dữ liệu
├── Predict_AQI.ipynb            # Xây dựng và đánh giá mô hình dự báo AQI
├── aqi_selected_cities.csv      # Dataset tổng hợp phục vụ phân tích
├── crawl_iqair.py               # Thu thập dữ liệu từ IQAir
├── merge_csv.py                 # Gộp các file dữ liệu
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 📊 Dữ liệu thu thập

Mỗi bản ghi có thể bao gồm các trường:

| Thuộc tính | Mô tả |
|---|---|
| `timestamp` | Thời gian lấy dữ liệu |
| `city` | Tên thành phố |
| `aqi` | Chỉ số chất lượng không khí |
| `weather` | Điều kiện thời tiết |
| `wind_speed` | Tốc độ gió |
| `humidity` | Độ ẩm |
| `temperature` | Nhiệt độ |
| `pm25` | Nồng độ bụi mịn PM2.5 |
| `pm10` | Nồng độ bụi PM10 |
| `o3` | Ozone |
| `no2` | Nitrogen dioxide |
| `so2` | Sulfur dioxide |
| `co` | Carbon monoxide |

Dữ liệu được cập nhật định kỳ và lưu dưới dạng CSV.

---

## 📈 Phân tích dữ liệu

Notebook `Phan_tich.ipynb` được sử dụng để thực hiện Exploratory Data Analysis (EDA), bao gồm:

- Kiểm tra dữ liệu thiếu.
- Thống kê mô tả các biến.
- Phân tích AQI theo giờ.
- Phân tích AQI theo ngày và tháng.
- So sánh chất lượng không khí giữa các thành phố.
- Phân tích xu hướng AQI theo thời gian.
- Xây dựng ma trận tương quan giữa AQI và các yếu tố môi trường.
- Trực quan hóa dữ liệu bằng biểu đồ.

Mục tiêu của bước này là hiểu đặc điểm dữ liệu trước khi đưa vào mô hình dự báo.

---

## 🧠 Dự báo AQI

Notebook `Predict_AQI.ipynb` được sử dụng để xây dựng và đánh giá các mô hình dự báo.

### Random Forest Regressor

Random Forest được sử dụng như một mô hình Machine Learning cơ sở để dự báo AQI từ các đặc trưng môi trường và đặc trưng thời gian.

Quy trình gồm:

- Tiền xử lý dữ liệu.
- Feature Engineering.
- Chia dữ liệu theo thứ tự thời gian.
- Time Series Cross Validation.
- Tối ưu tham số bằng `RandomizedSearchCV`.
- Đánh giá mô hình trên tập dữ liệu kiểm thử.

### LSTM

LSTM được thử nghiệm nhằm khai thác tính phụ thuộc theo thời gian của dữ liệu AQI.

Quy trình gồm:

- Chuẩn hóa dữ liệu.
- Chuyển dữ liệu thành chuỗi thời gian.
- Chia tập Train / Validation / Test.
- Huấn luyện mô hình LSTM.
- So sánh giá trị AQI dự báo với giá trị thực tế.

---

## 📏 Chỉ số đánh giá

Các mô hình được đánh giá bằng:

- **MAE — Mean Absolute Error**
- **MSE — Mean Squared Error**
- **RMSE — Root Mean Squared Error**
- **R² — Coefficient of Determination**

Những chỉ số này giúp đánh giá cả độ lệch trung bình và khả năng giải thích biến động của AQI.

---

## 🚀 Cài đặt và chạy dự án

Clone repository:

```bash
git clone https://github.com/dothang08/iqair-dataset.git
cd iqair-dataset
```

Cài đặt thư viện:

```bash
pip install -r requirements.txt
```

Chạy crawler:

```bash
python crawl_iqair.py
```

Gộp dữ liệu:

```bash
python merge_csv.py
```

Sau đó có thể mở các notebook:

```text
Phan_tich.ipynb
Predict_AQI.ipynb
```

bằng Jupyter Notebook, JupyterLab hoặc Google Colab.

---

## ⚙️ Tự động hóa bằng GitHub Actions

GitHub Actions được sử dụng để tự động chạy script thu thập dữ liệu theo chu kỳ.

Workflow nằm trong thư mục:

```text
.github/workflows/
```

Nhờ đó, dữ liệu có thể được cập nhật liên tục mà không cần chạy crawler thủ công.

---

## 💡 Hướng phát triển

Một số hướng có thể phát triển thêm:

- Bổ sung thêm thành phố và khu vực.
- Thu thập dữ liệu trong khoảng thời gian dài hơn.
- So sánh thêm các mô hình Machine Learning khác.
- Tối ưu mô hình LSTM.
- Xây dựng API dự báo AQI.
- Xây dựng dashboard theo dõi chất lượng không khí.
- Triển khai mô hình thành ứng dụng web.
- Bổ sung cảnh báo khi AQI vượt ngưỡng an toàn.

---

## ⚠️ Lưu ý

Dữ liệu của dự án được thu thập từ nguồn bên thứ ba và chủ yếu phục vụ cho mục đích học tập, nghiên cứu và phân tích.

Kết quả dự báo từ các mô hình Machine Learning không nên được xem là thông tin môi trường chính thức.

---

## 👨‍💻 Tác giả

**Đỗ Đức Thắng**

- GitHub: [dothang08](https://github.com/dothang08)
- Project: [iqair-dataset](https://github.com/dothang08/iqair-dataset)

---

## 🤝 Đóng góp

Mọi đóng góp đều được hoan nghênh.

Nếu bạn muốn cải thiện crawler, dữ liệu, notebook hoặc mô hình dự báo, hãy tạo:

- Issue
- Pull Request

---

## 🌱 Mục tiêu

> Biến dữ liệu môi trường thành thông tin có giá trị thông qua Python, Data Analysis và Machine Learning.

**Vì một tương lai xanh hơn. 🌿**
