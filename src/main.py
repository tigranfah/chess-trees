import tkinter as tk
from tkinter import messagebox
import chess
import chess.svg
from PIL import Image, ImageTk
import cairosvg
import io

class ChessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess GUI")
        self.width, self.height = 700, 700
        
        self.board = chess.Board()
        
        self.create_widgets()
        self.update_board_image()
    
    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()

        self.move_entry = tk.Entry(self.root)
        self.move_entry.pack()

        self.move_button = tk.Button(self.root, text="Make Move", command=self.make_move)
        self.move_button.pack()

    def make_move(self):
        move = self.move_entry.get()
        try:
            self.board.push_san(move)
            self.update_board_image()
        except ValueError:
            messagebox.showerror("Invalid Move", "The move is invalid. Please enter a valid move.")

    def update_board_image(self):
        svg_data = chess.svg.board(board=self.board).encode("utf-8")
        png_data = cairosvg.svg2png(bytestring=svg_data)
        
        image = Image.open(io.BytesIO(png_data))
        image = image.resize((self.width, self.height))
        photo = ImageTk.PhotoImage(image)

        self.canvas.image = photo
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessApp(root)
    root.mainloop()