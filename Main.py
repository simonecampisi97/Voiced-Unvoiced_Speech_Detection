from frontend.GUI import App
import tensorflow as tf

if __name__ == '__main__':

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    session = tf.Session(config=config)

    app = App()
    app.mainloop()
