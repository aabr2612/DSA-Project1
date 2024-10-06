import sys
import frontend.ui

if __name__=="__main__":
    app = frontend.ui.QApplication(sys.argv)
    window = frontend.ui.MainWindow()
    window.show()
    sys.exit(app.exec_())