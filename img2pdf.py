#!/usr/bin/env python3
import os
import sys
import gc
import argparse
from pathlib import Path
from PIL import Image
from tqdm import tqdm

def print_banner():
    print(r"""
   ___  __  ____  _  _  ____ 
  / __)(  )(  _ \( \/ )(  _ \ 
 ( (__  )(  )___/ )  (  )___/ 
  \___)(__)(__)  (__/)(__)  
Image-to-PDF Batch Converter
    """)

def get_supported_formats(args):
    base_formats = ['webp', 'jpg', 'jpeg', 'png']
    if not args.formats:
        return base_formats
    return [fmt.strip().lower() for fmt in args.formats.split(',') if fmt.strip().lower() in base_formats]

def batch_convert(args):
    supported_formats = get_supported_formats(args)
    files = []
    for fmt in supported_formats:
        files.extend(sorted(Path(args.input_dir).glob(f'*.{fmt}')))
    
    if not files:
        print("\033[31mNo supported images found!\033[0m")
        return

    output_path = Path(args.input_dir) / args.output if args.inplace else Path(args.output)
    
    temp_pdfs = []
    pbar = tqdm(range(0, len(files), args.batch_size), 
           desc="\033[36mProcessing\033[0m",
           unit="batch")
    for i in pbar:
        pbar.set_postfix_str(f"{min(i+args.batch_size, len(files))}/{len(files)} images")
        batch_files = files[i:i + args.batch_size]
        try:
            first_img = Image.open(batch_files[0]).convert('RGB')
            image_list = [Image.open(f).convert('RGB') for f in batch_files[1:]]
            
            temp_pdf = f"temp_{i}.pdf"
            first_img.save(temp_pdf, "PDF", resolution=100.0, save_all=True, append_images=image_list)
            temp_pdfs.append(temp_pdf)
        except Exception as e:
            print(f"\033[33mSkipping corrupt file: {batch_files[0]}\033[0m")
            continue
        
        del first_img, image_list
        gc.collect()

    from PyPDF2 import PdfMerger
    merger = PdfMerger()
    for pdf in temp_pdfs:
        merger.append(pdf)
    merger.write(str(output_path))
    merger.close()
    
    for pdf in temp_pdfs:
        os.remove(pdf)
    print(f"\033[32mSuccess! PDF saved to:\033[0m {output_path.resolve()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-dir', required=True, help="Directory containing image files")
    parser.add_argument('-o', '--output', default="output.pdf", help="Output PDF filename")
    parser.add_argument('-b', '--batch-size', type=int, default=20, help="Images per batch")
    parser.add_argument('-f', '--formats', help="Comma-separated formats (webp,jpg,png)")
    parser.add_argument('--inplace', action='store_true', help="Save PDF inside input directory")
    args = parser.parse_args()
    
    batch_convert(args)
