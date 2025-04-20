import tkinter as tk
from tkinter import filedialog, ttk, messagebox,Tk, Label, PhotoImage,simpledialog
from PIL import Image, ImageTk, ImageDraw  # Import Pillow classes
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from fpdf import FPDF
import sqlite3
import csv
import os
from tkcalendar import DateEntry  # Import DateEntry
import sys
from io import BytesIO


############################ Init ########################################################

def main():
    DNA = {"ABC,AFG,ASS"}
    name = input("Enter your Gene: ")
    if(name != DNA):
        print("mutation")



if __name__ == "__main__":
    main()  # Start with the login window
