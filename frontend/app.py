import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import requests

class RAGClient:

    def __init__(self):
        self.api_base = "http://localhost:8000"

        self.root = tk.Tk()
        self.root.title("📚 RAG Assistant - PDF Q&A")
        self.root.geometry("900x700")
        self.root.minsize(700, 500)

        # GUI Colors
        self.bg_color = "#2C3E50"
        self.fg_color = "#ECF0F1"
        self.accent_color = "#3498DB"
        self.button_color = "#27AE60"

        self.root.configure(bg=self.bg_color)

        # Variables
        self.pdf_loaded = False

        # Check API connection
        self.check_api_connection()

        # GUI
        self.create_widgets()

    def check_api_connection(self):
        try:
            response = requests.get(f"{self.api_base}/health", timeout=2)
            if response.status_code != 200:
                messagebox.showerror("Error", "⚠️ API not available")
                self.root.quit()
        except:
            messagebox.showerror("Error", "⚠️ Cant connecto to API")
            self.root.quit()

    def create_widgets(self):
        # Grid
        self.root.rowconfigure(3, weight=1)
        self.root.columnconfigure(0, weight=1)

        # -- Header --
        header = tk.Frame(self.root, bg=self.accent_color, height=60)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        
        title = tk.Label(header, text="📚 RAG Assistant", 
                        font=("Arial", 20, "bold"), 
                        bg=self.accent_color, fg="white")
        title.pack(pady=15)

        # -- Actions --
        action_frame = tk.Frame(self.root, bg=self.bg_color)
        action_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=20)

        # Button load PDF
        self.load_btn = tk.Button(action_frame, text="📄 Load PDF", command=self.upload_pdf_thread, bg=self.accent_color, fg="white", font=("Arial", 11, "bold"), width=15, height=2)
        self.load_btn.pack(side="left", padx=5)

        # Info PDF
        self.pdf_info_label = tk.Label(action_frame, text="No PDF loaded", bg=self.bg_color, fg="#95A5A6", font=("Arial", 10))
        self.pdf_info_label.pack(side="left", padx=15)

        # Botón limpiar BD
        self.clear_btn = tk.Button(action_frame, text="🗑️ Clear Database", command=self.clear_database, bg="#E74C3C", fg="white", font=("Arial", 10))
        self.clear_btn.pack(side="right", padx=5)

        # -- Query --
        query_frame = tk.Frame(self.root, bg=self.bg_color)
        query_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)

        tk.Label(query_frame, text="Search in PDF:", bg=self.bg_color, fg=self.fg_color, font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 5))

        query_input_frame = tk.Frame(query_frame, bg=self.bg_color)
        query_input_frame.pack(fill="x", pady=5)

        self.query_box = tk.Entry(query_input_frame, font=("Arial", 11))
        self.query_box.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.query_box.bind("<Return>", lambda e: self.search_query())

        self.search_btn = tk.Button(query_input_frame, text="🔍 Search", command=self.search_query, bg=self.button_color, fg="white", font=("Arial", 10, "bold"), width=12)
        self.search_btn.pack(side="left")

        # Number of results
        results_config = tk.Frame(query_frame, bg=self.bg_color)
        results_config.pack(fill="x", pady=5)

        tk.Label(results_config, text="Results to show:", bg=self.bg_color, fg=self.fg_color, font=("Arial", 10)).pack(side="left", padx=(0, 10))

        self.num_results = tk.Spinbox(results_config, from_=1, to=10, width=10, font=("Arial", 10), buttonbackground=self.accent_color)
        self.num_results.delete(0, tk.END)
        self.num_results.insert(0, "3")
        self.num_results.pack(side="left", padx=5)

        # -- Result --
        result_frame = tk.Frame(self.root, bg=self.bg_color)
        result_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.root.rowconfigure(3, weight=1)

        tk.Label(result_frame, text="Results:",  bg=self.bg_color, fg=self.fg_color, font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 5))

        # Text scrollbar
        text_frame = tk.Frame(result_frame)
        text_frame.pack(fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        self.output = tk.Text(text_frame, wrap="word", font=("Arial", 10), yscrollcommand=scrollbar.set, bg="#34495E", fg="white", padx=10, pady=10)
        self.output.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.output.yview)

        # Mensaje inicial
        self.output.insert("1.0", "👋 Welcome to RAG Assistant!\n\n" +
                          "🔗 Connected to API: " + self.api_base + "\n\n" +
                          "📖 How to use:\n" +
                          "  1. Click 'Upload PDF' to upload a document\n" +
                          "  2. Wait for processing\n" +
                          "  3. Type your search query\n" +
                          "  4. Press Enter or click 'Search'\n\n" +
                          "💡 The API will find the most relevant sections!")
        self.output.config(state="disabled")

    def lock_ui(self):
        self.load_btn.config(state="disabled")
        self.search_btn.config(state="disabled")
        self.clear_btn.config(state="disabled")

    def unlock_ui(self):
        self.load_btn.config(state="normal")
        self.search_btn.config(state="normal")
        self.clear_btn.config(state="normal")

    def upload_pdf_thread(self):
        thread = threading.Thread(target=self.upload_pdf, daemon=True)
        thread.start()

    def upload_pdf(self):
        path = filedialog.askopenfilename(
            title="Select PDF",
            filetypes=[("PDF files", "*.pdf")]
        )
        if not path:
            return
        
        self.lock_ui()
        self.update_output("⏳ Uploading PDF to server...\n")
        
        try:
            # Subir archivo
            with open(path, 'rb') as f:
                files = {'file': (path.split('/')[-1], f, 'application/pdf')}
                response = requests.post(f"{self.api_base}/upload-pdf", files=files)
            
            if response.status_code == 200:
                data = response.json()
                
                self.pdf_loaded = True
                filename = data['filename']
                chunks = data['chunks_count']
                
                self.pdf_info_label.config(
                    text=f"✅ {filename} ({chunks} chunks)",
                    fg="#27AE60"
                )
                
                self.update_output(f"✅ PDF uploaded successfully!\n\n" +
                                 f"📊 Statistics:\n" +
                                 f"  • File: {filename}\n" +
                                 f"  • Chunks: {chunks}\n\n" +
                                 f"🎯 Ready to search!")
            else:
                error = response.json().get('detail', 'Unknown error')
                messagebox.showerror("Error", f"❌ {error}")
                self.update_output(f"❌ Error: {error}\n")
        
        except Exception as e:
            messagebox.showerror("Error", f"❌ {str(e)}")
            self.update_output(f"❌ Error: {str(e)}\n")
        
        finally:
            self.unlock_ui()

    def search_query(self):
        if not self.pdf_loaded:
            messagebox.showwarning("Warning", "⚠️ Upload a PDF first!")
            return
        
        query = self.query_box.get().strip()
        if not query:
            messagebox.showwarning("Warning", "⚠️ Write a search query")
            return
        
        self.lock_ui()
        self.update_output(f"🔍 Searching: '{query}'\n\n")
        
        try:
            # Call API
            num_results = int(self.num_results.get())
            payload = {
                "query": query,
                "top_k": num_results
            }
            
            response = requests.post(f"{self.api_base}/search", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                chunks = data['chunks']
                distances = data['distances']
                
                # Show results
                output_text = f"🔍 Query: '{query}'\n"
                output_text += f"📊 Found {len(chunks)} relevant chunks:\n\n"
                output_text += "=" * 60 + "\n\n"
                
                for i, (chunk, distance) in enumerate(zip(chunks, distances), 1):
                    similarity = 1 - distance
                    output_text += f"📄 Result {i} (Similarity: {similarity:.2%})\n"
                    output_text += "─" * 60 + "\n"
                    output_text += f"{chunk}\n\n"
                    output_text += "=" * 60 + "\n\n"
                
                self.update_output(output_text)
            else:
                error = response.json().get('detail', 'Unknown error')
                messagebox.showerror("Error", f"❌ {error}")
                self.update_output(f"❌ Error: {error}\n")
        
        except Exception as e:
            messagebox.showerror("Error", f"❌ {str(e)}")
            self.update_output(f"❌ Error: {str(e)}\n")
        
        finally:
            self.unlock_ui()

    def clear_database(self):
        response = messagebox.askyesno(
            "Confirm", 
            "🗑️ This will delete all stored documents.\n\nAre you sure?"
        )
        
        if response:
            try:
                resp = requests.delete(f"{self.api_base}/clear")
                
                if resp.status_code == 200:
                    self.pdf_loaded = False
                    self.pdf_info_label.config(text="No documents loaded", fg="#95A5A6")
                    
                    self.update_output("✅ Database cleared successfully!\n\n" +
                                     "Upload a new PDF to start.")
                    
                    messagebox.showinfo("Success", "✅ Database cleared!")
                else:
                    messagebox.showerror("Error", "Error clearing database")
            
            except Exception as e:
                messagebox.showerror("Error", f"❌ {str(e)}")

    def update_output(self, text):
        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.insert("1.0", text)
        self.output.config(state="disabled")
        self.root.update()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    RAGClient().run()