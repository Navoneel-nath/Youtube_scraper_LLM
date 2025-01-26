from ui.gradio_interface import create_interface

if __name__ == "__main__":
    interface = create_interface()
    interface.launch(share=True, server_port=7860)