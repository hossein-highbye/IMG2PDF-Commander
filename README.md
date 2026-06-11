# 🚀 WEBP2PDF Commander  
*A memory-efficient batch image converter for Android (Termux) and desktop*  

📦 **Features**  
- Converts WEBP/JPG/PNG to PDF in memory-safe batches  
- Progress tracking with image/batch counters  
- Optional format filtering  
- Works on Termux (Android) and desktop  

🛠️ **Installation**  
```bash
pip install -r requirements.txt
```

🎮 **Usage**  
```bash
# Convert all supported images in a directory  
python converttopdf.py -i /path/to/images  

# Specific formats only  
python converttopdf.py -i /path/to/images -f webp,jpg  

# Save PDF inside source folder  
python converttopdf.py -i /path/to/images --inplace  
```  

❓ **Troubleshooting**  
- `UnboundLocalError`: Update to the latest script version  
- Permission issues: Run `termux-setup-storage` first
