import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import os
from tkinter.scrolledtext import ScrolledText
from collections import Counter

class AlumniDatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Alumni Matematika FMIPA UI")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f2f5')
        
        # Data storage
        self.alumni_data = pd.DataFrame()
        self.filtered_data = pd.DataFrame()
        
        # Search filters
        self.search_vars = {
            'nama': tk.StringVar(),
            'program_studi': tk.StringVar(),
            'npm': tk.StringVar(),
            'pekerjaan': tk.StringVar(),
            'perusahaan': tk.StringVar(),
            'gaji': tk.StringVar()
        }
        
        # Bind search filters to update function
        for var in self.search_vars.values():
            var.trace('w', self.update_filtered_data)
        
        # Current page
        self.current_page = 'welcome'
        self.selected_alumni = None
        
        # Load data and show welcome page
        self.load_data()
        self.show_welcome_page()
    
    def load_data(self):
        """Load alumni data from Excel file"""
        try:
            # Try to load the Excel file
            file_path = "C:\\Users\\USER HP\\Downloads\\gui\\gui\\Database Alumni S1 Departemen Matematika FMIPA UI (1).xlsx"
            if os.path.exists(file_path):
                self.alumni_data = pd.read_excel(file_path, sheet_name='Data ')
                # Format data
                self.alumni_data['NPM'] = self.alumni_data['NPM'].astype(str)
                self.alumni_data['Angkatan'] = self.alumni_data['Angkatan'].astype(str)
                self.alumni_data['Tahun Lulus'] = self.alumni_data['Tahun Lulus'].astype(str)
                self.alumni_data['Rata-rata Gaji'] = self.alumni_data['Rata-rata Gaji'].apply(self.format_currency)
                self.filtered_data = self.alumni_data.copy()
            else:
                # Sample data if file not found
                sample_data = {
                    'No': [1, 2, 3],
                    'Nama': ['Sari Gita Fitri', 'Natasha Rosaline', 'Fadel Muhammad'],
                    'NPM': ['1606829390', '1606889793', '1606824540'],
                    'Program Studi': ['Matematika', 'Matematika', 'Matematika'],
                    'Angkatan': ['2016', '2016', '2016'],
                    'Peminatan': ['Matematika Komputasi', 'Matematika Komputasi', 'Matematika Komputasi'],
                    'Judul Skripsi': [
                        'Implementasi Algoritma Kernel K-Means based Co-clustering untuk Memprediksi Penyakit Kanker Paru-paru',
                        'Fuzzy C-Means Clustering dengan Reduksi Dimensi Deep Autoencoders untuk Pendeteksian Topik pada Data Tekstual Twitter',
                        'Prediksi Insiden DBD di DKI Jakarta Menggunakan Radial Basis Function Neural Network'
                    ],
                    'Tahun Lulus': ['2020', '2020', '2020'],
                    'Pekerjaan': ['Data Analyst', 'Senior Analyst Specialist System Infrastructure', 'Data Platform Engineer'],
                    'Id Karyawan': ['KI202001', 'BC202049', 'BR202070'],
                    'Nama Perusahaan': ['Kimbo', 'PT Bank Central Asia Tbk', 'PT Bank Raya Indonesia'],
                    'Alamat Perusahaan': [
                        'Ruko Harco Mangga Dua, Jakarta',
                        'Menara BCA lantai LG. Jl. MH. Thamrin no. 1 Jakarta Pusat 10310',
                        'Jl. Jenderal Sudirman Kav.44-46, Jakarta 10210'
                    ],
                    'Rata-rata Gaji': ['Rp8.000.000,00', 'Rp15.000.000,00', 'Rp12.000.000,00']
                }
                self.alumni_data = pd.DataFrame(sample_data)
                self.filtered_data = self.alumni_data.copy()
                messagebox.showwarning("File Not Found", "Excel file not found. Using sample data.")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {str(e)}")
    
    def format_currency(self, amount):
        """Format currency from number to Rupiah format"""
        if pd.isna(amount) or amount == '':
            return 'Tidak tersedia'
        try:
            if isinstance(amount, str) and amount.startswith('Rp'):
                return amount
            num_amount = int(float(amount))
            return f"Rp{num_amount:,}".replace(',', '.') + ",00"
        except:
            return str(amount)
    
    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_welcome_page(self):
        """Display welcome page"""
        self.current_page = 'welcome'
        self.clear_window()
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2563eb')
        main_frame.pack(fill='both', expand=True)
        
        # Welcome content
        welcome_frame = tk.Frame(main_frame, bg='#2563eb')
        welcome_frame.pack(expand=True)
        
        # Title
        title_label = tk.Label(welcome_frame, text="Database Alumni", 
                              font=('Arial', 32, 'bold'), fg='white', bg='#2563eb')
        title_label.pack(pady=(50, 10))
        
        subtitle_label = tk.Label(welcome_frame, text="Departemen Matematika FMIPA UI", 
                                 font=('Arial', 24, 'bold'), fg='white', bg='#2563eb')
        subtitle_label.pack(pady=(0, 20))
        
        desc_label = tk.Label(welcome_frame, 
                             text="Sistem informasi terintegrasi untuk mengelola data alumni\nSarjana Matematika, Statistika, dan Ilmu Aktuaria", 
                             font=('Arial', 14), fg='white', bg='#2563eb', justify='center')
        desc_label.pack(pady=(0, 50))
        
        # Features frame
        features_frame = tk.Frame(welcome_frame, bg='#2563eb')
        features_frame.pack(pady=(0, 50))
        
        features = [
            ("📊 Data Alumni", "Pencarian dan pengelolaan\ndata lengkap alumni"),
            ("🏢 Perusahaan", "Analisis distribusi alumni\ndi berbagai perusahaan"),
            ("📈 Statistik", "Laporan dan analisis\ndata karir alumni")
        ]
        
        for i, (title, desc) in enumerate(features):
            feature_frame = tk.Frame(features_frame, bg='#3b82f6', relief='raised', bd=2)
            feature_frame.grid(row=0, column=i, padx=20, pady=20, ipadx=20, ipady=20)
            
            tk.Label(feature_frame, text=title, font=('Arial', 14, 'bold'), 
                    fg='white', bg='#3b82f6').pack()
            tk.Label(feature_frame, text=desc, font=('Arial', 10), 
                    fg='white', bg='#3b82f6', justify='center').pack(pady=(10, 0))
        
        # Start button
        start_btn = tk.Button(welcome_frame, text="Mulai Eksplorasi Data", 
                             font=('Arial', 16, 'bold'), bg='white', fg='#2563eb',
                             padx=30, pady=15, command=self.show_search_page)
        start_btn.pack(pady=(30, 0))
    
    def show_search_page(self):
        """Display search and data page"""
        self.current_page = 'search'
        self.clear_window()
        
        # Header
        header_frame = tk.Frame(self.root, bg='white', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg='white')
        header_content.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(header_content, text="Database Alumni Matematika FMIPA UI", 
                font=('Arial', 18, 'bold'), bg='white').pack(side='left')
        
        # Navigation buttons
        nav_frame = tk.Frame(header_content, bg='white')
        nav_frame.pack(side='right')
        
        tk.Button(nav_frame, text="🏠 Beranda", command=self.show_welcome_page,
                 bg='#f3f4f6', pady=5, padx=10).pack(side='left', padx=5)
        tk.Button(nav_frame, text="📊 Statistik", command=self.show_statistics_page,
                 bg='#f3f4f6', pady=5, padx=10).pack(side='left', padx=5)
        tk.Button(nav_frame, text="➕ Tambah Data", command=self.show_add_form,
                 bg='#2563eb', fg='white', pady=5, padx=10).pack(side='left', padx=5)
        
        # Main content
        main_frame = tk.Frame(self.root, bg='#f0f2f5')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Search filters
        self.create_search_filters(main_frame)
        
        # Results table
        self.create_results_table(main_frame)
    
    def create_search_filters(self, parent):
        """Create search filter widgets"""
        filter_frame = tk.LabelFrame(parent, text="🔍 Pencarian Alumni", 
                                    font=('Arial', 12, 'bold'), bg='white', padx=10, pady=10)
        filter_frame.pack(fill='x', pady=(0, 20))
        
        # Filter controls frame
        controls_frame = tk.Frame(filter_frame, bg='white')
        controls_frame.pack(fill='x')
        
        # Clear button
        tk.Button(controls_frame, text="Hapus Semua Filter", 
                 command=self.clear_all_filters, bg='#ef4444', fg='white',
                 pady=5, padx=10).pack(side='right')
        
        # Filter inputs
        filters_frame = tk.Frame(filter_frame, bg='white')
        filters_frame.pack(fill='x', pady=(10, 0))
        
        # First row
        row1 = tk.Frame(filters_frame, bg='white')
        row1.pack(fill='x', pady=5)
        
        tk.Label(row1, text="Nama:", bg='white', width=12, anchor='w').grid(row=0, column=0, padx=5)
        tk.Entry(row1, textvariable=self.search_vars['nama'], width=25).grid(row=0, column=1, padx=5)
        
        tk.Label(row1, text="Program Studi:", bg='white', width=12, anchor='w').grid(row=0, column=2, padx=5)
        program_combo = ttk.Combobox(row1, textvariable=self.search_vars['program_studi'], width=22,
                                   values=['', 'Matematika', 'Statistika', 'Ilmu Aktuaria'])
        program_combo.grid(row=0, column=3, padx=5)
        
        tk.Label(row1, text="NPM:", bg='white', width=12, anchor='w').grid(row=0, column=4, padx=5)
        tk.Entry(row1, textvariable=self.search_vars['npm'], width=25).grid(row=0, column=5, padx=5)
        
        # Second row
        row2 = tk.Frame(filters_frame, bg='white')
        row2.pack(fill='x', pady=5)
        
        tk.Label(row2, text="Pekerjaan:", bg='white', width=12, anchor='w').grid(row=0, column=0, padx=5)
        tk.Entry(row2, textvariable=self.search_vars['pekerjaan'], width=25).grid(row=0, column=1, padx=5)
        
        tk.Label(row2, text="Perusahaan:", bg='white', width=12, anchor='w').grid(row=0, column=2, padx=5)
        tk.Entry(row2, textvariable=self.search_vars['perusahaan'], width=25).grid(row=0, column=3, padx=5)
        
        tk.Label(row2, text="Gaji:", bg='white', width=12, anchor='w').grid(row=0, column=4, padx=5)
        tk.Entry(row2, textvariable=self.search_vars['gaji'], width=25).grid(row=0, column=5, padx=5)
    
    def create_results_table(self, parent):
        """Create results table with alumni data"""
        results_frame = tk.LabelFrame(parent, text=f"Hasil Pencarian ({len(self.filtered_data)} alumni)", 
                                     font=('Arial', 12, 'bold'), bg='white', padx=10, pady=10)
        results_frame.pack(fill='both', expand=True)
        
        # Table frame with scrollbars
        table_frame = tk.Frame(results_frame, bg='white')
        table_frame.pack(fill='both', expand=True)
        
        # Treeview for data display
        columns = ['Nama', 'NPM', 'Program Studi', 'Pekerjaan', 'Nama Perusahaan', 'Rata-rata Gaji']
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Define column headings and widths
        column_widths = {'Nama': 150, 'NPM': 120, 'Program Studi': 120, 
                        'Pekerjaan': 200, 'Nama Perusahaan': 180, 'Rata-rata Gaji': 130}
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths[col], minwidth=100)
        
        # Scrollbars
        y_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        x_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        # Pack table and scrollbars
        self.tree.pack(side='left', fill='both', expand=True)
        y_scrollbar.pack(side='right', fill='y')
        x_scrollbar.pack(side='bottom', fill='x')
        
        # Bind double-click to show details
        self.tree.bind('<Double-1>', self.show_alumni_detail)
        
        # Update table with data
        self.update_table()
    
    def update_filtered_data(self, *args):
        """Update filtered data based on search criteria"""
        if self.alumni_data.empty:
            return
            
        filtered = self.alumni_data.copy()
        
        # Apply filters
        if self.search_vars['nama'].get():
            filtered = filtered[filtered['Nama'].str.contains(self.search_vars['nama'].get(), case=False, na=False)]
        
        if self.search_vars['program_studi'].get():
            filtered = filtered[filtered['Program Studi'].str.contains(self.search_vars['program_studi'].get(), case=False, na=False)]
        
        if self.search_vars['npm'].get():
            filtered = filtered[filtered['NPM'].str.contains(self.search_vars['npm'].get(), na=False)]
        
        if self.search_vars['pekerjaan'].get():
            filtered = filtered[filtered['Pekerjaan'].str.contains(self.search_vars['pekerjaan'].get(), case=False, na=False)]
        
        if self.search_vars['perusahaan'].get():
            filtered = filtered[filtered['Nama Perusahaan'].str.contains(self.search_vars['perusahaan'].get(), case=False, na=False)]
        
        if self.search_vars['gaji'].get():
            filtered = filtered[filtered['Rata-rata Gaji'].str.contains(self.search_vars['gaji'].get(), case=False, na=False)]
        
        self.filtered_data = filtered
        
        # Update table if on search page
        if self.current_page == 'search':
            self.update_table()
            # Update results count
            for widget in self.root.winfo_children():
                for child in widget.winfo_children():
                    if isinstance(child, tk.LabelFrame) and "Hasil Pencarian" in child.cget('text'):
                        child.configure(text=f"Hasil Pencarian ({len(self.filtered_data)} alumni)")
    
    def update_table(self):
        """Update the treeview table with filtered data"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insert filtered data
        for idx, row in self.filtered_data.iterrows():
            values = [row['Nama'], row['NPM'], row['Program Studi'], 
                     row['Pekerjaan'], row['Nama Perusahaan'], row['Rata-rata Gaji']]
            self.tree.insert('', 'end', values=values)
    
    def clear_all_filters(self):
        """Clear all search filters"""
        for var in self.search_vars.values():
            var.set('')
    
    def show_alumni_detail(self, event):
        """Show detailed information for selected alumni"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        nama = item['values'][0]
        
        # Find alumni in data
        alumni = self.alumni_data[self.alumni_data['Nama'] == nama].iloc[0]
        self.selected_alumni = alumni
        
        # Create detail window
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Detail Alumni - {nama}")
        detail_window.geometry("800x600")
        detail_window.configure(bg='#f0f2f5')
        
        # Header
        header_frame = tk.Frame(detail_window, bg='white', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text=f"Detail Alumni - {nama}", 
                font=('Arial', 18, 'bold'), bg='white').pack(pady=20)
        
        # Content frame
        content_frame = tk.Frame(detail_window, bg='#f0f2f5')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Alumni info frame
        info_frame = tk.LabelFrame(content_frame, text="👤 Informasi Alumni", 
                                  font=('Arial', 12, 'bold'), bg='white', padx=15, pady=15)
        info_frame.pack(fill='x', pady=(0, 20))
        
        # Basic info
        basic_info = tk.Frame(info_frame, bg='white')
        basic_info.pack(fill='x')
        
        tk.Label(basic_info, text=f"Nama: {alumni['Nama']}", 
                font=('Arial', 12, 'bold'), bg='white', anchor='w').pack(fill='x', pady=2)
        tk.Label(basic_info, text=f"NPM: {alumni['NPM']}", 
                font=('Arial', 10), bg='white', anchor='w').pack(fill='x', pady=2)
        
        # Education frame
        edu_frame = tk.LabelFrame(content_frame, text="📚 Riwayat Pendidikan", 
                                 font=('Arial', 12, 'bold'), bg='white', padx=15, pady=15)
        edu_frame.pack(fill='x', pady=(0, 20))
        
        edu_info = [
            f"Program Studi: {alumni['Program Studi']}",
            f"Peminatan: {alumni['Peminatan']}",
            f"Angkatan: {alumni['Angkatan']}",
            f"Tahun Lulus: {alumni['Tahun Lulus']}",
            f"Judul Skripsi: {alumni['Judul Skripsi']}"
        ]
        
        for info in edu_info:
            tk.Label(edu_frame, text=info, font=('Arial', 10), bg='white', 
                    anchor='w', wraplength=700, justify='left').pack(fill='x', pady=2)
        
        # Career frame
        career_frame = tk.LabelFrame(content_frame, text="💼 Informasi Karir", 
                                    font=('Arial', 12, 'bold'), bg='white', padx=15, pady=15)
        career_frame.pack(fill='both', expand=True)
        
        career_info = [
            f"Pekerjaan: {alumni['Pekerjaan']}",
            f"Perusahaan: {alumni['Nama Perusahaan']}",
            f"ID Karyawan: {alumni['Id Karyawan']}",
            f"Alamat Perusahaan: {alumni['Alamat Perusahaan']}",
            f"Rata-rata Gaji: {alumni['Rata-rata Gaji']}"
        ]
        
        for info in career_info:
            tk.Label(career_frame, text=info, font=('Arial', 10), bg='white', 
                    anchor='w', wraplength=700, justify='left').pack(fill='x', pady=2)
    
    def show_statistics_page(self):
        """Display statistics page"""
        self.current_page = 'statistics'
        self.clear_window()
        
        # Header
        header_frame = tk.Frame(self.root, bg='white', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg='white')
        header_content.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(header_content, text="Statistik Alumni", 
                font=('Arial', 18, 'bold'), bg='white').pack(side='left')
        
        tk.Button(header_content, text="← Kembali ke Pencarian", 
                 command=self.show_search_page, bg='#f3f4f6', pady=5, padx=10).pack(side='right')
        
        # Main content
        main_frame = tk.Frame(self.root, bg='#f0f2f5')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Statistics cards
        stats_frame = tk.Frame(main_frame, bg='#f0f2f5')
        stats_frame.pack(fill='x', pady=(0, 20))
        
        # Total alumni card
        total_card = tk.Frame(stats_frame, bg='white', relief='raised', bd=2)
        total_card.pack(side='left', fill='both', expand=True, padx=(0, 10), pady=10, ipadx=20, ipady=20)
        
        tk.Label(total_card, text="Total Alumni", font=('Arial', 12), bg='white', fg='#6b7280').pack()
        tk.Label(total_card, text=str(len(self.alumni_data)), font=('Arial', 24, 'bold'), 
                bg='white', fg='#1f2937').pack()
        
        # Program studi card
        program_card = tk.Frame(stats_frame, bg='white', relief='raised', bd=2)
        program_card.pack(side='left', fill='both', expand=True, padx=10, pady=10, ipadx=20, ipady=20)
        
        unique_programs = self.alumni_data['Program Studi'].nunique()
        tk.Label(program_card, text="Program Studi", font=('Arial', 12), bg='white', fg='#6b7280').pack()
        tk.Label(program_card, text=str(unique_programs), font=('Arial', 24, 'bold'), 
                bg='white', fg='#1f2937').pack()
        
        # Companies card
        company_card = tk.Frame(stats_frame, bg='white', relief='raised', bd=2)
        company_card.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10, ipadx=20, ipady=20)
        
        unique_companies = self.alumni_data['Nama Perusahaan'].nunique()
        tk.Label(company_card, text="Perusahaan", font=('Arial', 12), bg='white', fg='#6b7280').pack()
        tk.Label(company_card, text=str(unique_companies), font=('Arial', 24, 'bold'), 
                bg='white', fg='#1f2937').pack()
        
        # Top companies
        top_companies_frame = tk.LabelFrame(main_frame, text="🏆 Top 3 Perusahaan Paling Populer", 
                                           font=('Arial', 12, 'bold'), bg='white', padx=15, pady=15)
        top_companies_frame.pack(fill='both', expand=True)
        
        # Calculate top companies
        company_counts = Counter(self.alumni_data['Nama Perusahaan'].dropna())
        top_companies = company_counts.most_common(3)
        
        medals = ['🥇', '🥈', '🥉']
        colors = ['#fbbf24', '#9ca3af', '#f97316']
        
        for i, (company, count) in enumerate(top_companies):
            company_frame = tk.Frame(top_companies_frame, bg='#f9fafb', relief='raised', bd=1)
            company_frame.pack(fill='x', pady=5, padx=10, ipady=10)
            
            # Rank
            rank_frame = tk.Frame(company_frame, bg='#f9fafb')
            rank_frame.pack(side='left', padx=10)
            
            tk.Label(rank_frame, text=medals[i], font=('Arial', 20), bg='#f9fafb').pack()
            
            # Company info
            info_frame = tk.Frame(company_frame, bg='#f9fafb')
            info_frame.pack(side='left', fill='x', expand=True, padx=10)
            
            tk.Label(info_frame, text=company, font=('Arial', 14, 'bold'), 
                    bg='#f9fafb', anchor='w').pack(fill='x')
            tk.Label(info_frame, text=f"{count} alumni bekerja di sini", 
                    font=('Arial', 10), bg='#f9fafb', fg='#6b7280', anchor='w').pack(fill='x')
            
            # Percentage
            percentage = (count / len(self.alumni_data)) * 100
            percent_frame = tk.Frame(company_frame, bg=colors[i], relief='raised', bd=1)
            percent_frame.pack(side='right', padx=10, pady=5, ipadx=10, ipady=5)
            
            tk.Label(percent_frame, text=f"{percentage:.1f}%", 
                    font=('Arial', 12, 'bold'), bg=colors[i], fg='white').pack()
    
    def show_add_form(self):
        """Show form to add new alumni data"""
        add_window = tk.Toplevel(self.root)
        add_window.title("Tambah Data Alumni Baru")
        add_window.geometry("700x700")
        add_window.configure(bg='#f0f2f5')
        
        # Header
        header_frame = tk.Frame(add_window, bg='white', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="Tambah Data Alumni Baru", 
                font=('Arial', 16, 'bold'), bg='white').pack(pady=15)
        
        # Form frame with scrollbar
        canvas = tk.Canvas(add_window, bg='#f0f2f5')
        scrollbar = ttk.Scrollbar(add_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f2f5')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Form fields
        form_frame = tk.Frame(scrollable_frame, bg='white', padx=20, pady=20)
        form_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Form variables
        form_vars = {
            'Nama': tk.StringVar(),
            'NPM': tk.StringVar(),
            'Program Studi': tk.StringVar(),
            'Angkatan': tk.StringVar(),
            'Peminatan': tk.StringVar(),
            'Judul Skripsi': tk.StringVar(),
            'Tahun Lulus': tk.StringVar(),
            'Pekerjaan': tk.StringVar(),
            'Id Karyawan': tk.StringVar(),
            'Nama Perusahaan': tk.StringVar(),
            'Alamat Perusahaan': tk.StringVar(),
            'Rata-rata Gaji': tk.StringVar()
        }
        
        # Create form fields
        row = 0
        for field, var in form_vars.items():
            tk.Label(form_frame, text=f"{field}:", font=('Arial', 10, 'bold'), 
                    bg='white', anchor='w').grid(row=row, column=0, sticky='w', pady=5, padx=(0, 10))
            
            if field == 'Program Studi':
                combo = ttk.Combobox(form_frame, textvariable=var, width=40,
                                   values=['Matematika', 'Statistika', 'Ilmu Aktuaria'])
                combo.grid(row=row, column=1, sticky='w', pady=5)
            elif field in ['Judul Skripsi', 'Alamat Perusahaan']:
                text_widget = tk.Text(form_frame, width=45, height=3, font=('Arial', 9))
                text_widget.grid(row=row, column=1, sticky='w', pady=5)
                
                # Bind text widget to variable
                def update_var(event, var=var, widget=text_widget):
                    var.set(widget.get("1.0", "end-1c"))
                text_widget.bind('<KeyRelease>', update_var)
            else:
                entry = tk.Entry(form_frame, textvariable=var, width=45, font=('Arial', 9))
                entry.grid(row=row, column=1, sticky='w', pady=5)
                
                # Special handling for salary field
                if field == 'Rata-rata Gaji':
                    tk.Label(form_frame, text="(Masukkan angka saja, contoh: 8000000)", 
                            font=('Arial', 8), bg='white', fg='#6b7280').grid(row=row+1, column=1, sticky='w')
                    row += 1
            
            row += 1
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg='white')
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        def save_alumni():
            # Validate required fields
            required_fields = ['Nama', 'NPM', 'Program Studi']
            for field in required_fields:
                if not form_vars[field].get().strip():
                    messagebox.showerror("Error", f"Field {field} harus diisi!")
                    return
            
            # Format salary
            gaji_str = form_vars['Rata-rata Gaji'].get().strip()
            if gaji_str:
                try:
                    gaji_num = int(gaji_str.replace('.', '').replace(',', ''))
                    formatted_gaji = self.format_currency(gaji_num)
                    form_vars['Rata-rata Gaji'].set(formatted_gaji)
                except ValueError:
                    if not gaji_str.startswith('Rp'):
                        messagebox.showerror("Error", "Format gaji tidak valid!")
                        return
            
            # Create new alumni record
            new_alumni = {}
            for field, var in form_vars.items():
                if field in ['Judul Skripsi', 'Alamat Perusahaan']:
                    # Get value from text widget
                    for widget in form_frame.winfo_children():
                        if isinstance(widget, tk.Text):
                            new_alumni[field] = widget.get("1.0", "end-1c")
                            break
                else:
                    new_alumni[field] = var.get()
            
            new_alumni['No'] = len(self.alumni_data) + 1
            
            # Add to dataframe
            new_row = pd.DataFrame([new_alumni])
            self.alumni_data = pd.concat([self.alumni_data, new_row], ignore_index=True)
            self.filtered_data = self.alumni_data.copy()
            
            messagebox.showinfo("Success", "Data alumni berhasil ditambahkan!")
            add_window.destroy()
            
            # Refresh search page if currently viewing
            if self.current_page == 'search':
                self.show_search_page()
        
        tk.Button(button_frame, text="Simpan Data", command=save_alumni,
                 bg='#2563eb', fg='white', font=('Arial', 12, 'bold'), 
                 padx=20, pady=10).pack(side='left', padx=10)
        tk.Button(button_frame, text="Batal", command=add_window.destroy,
                 bg='#6b7280', fg='white', font=('Arial', 12, 'bold'), 
                 padx=20, pady=10).pack(side='left', padx=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = AlumniDatabaseApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()