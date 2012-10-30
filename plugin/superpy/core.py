import vim
import utils


def get_super():
    row, col = vim.current.window.cursor
    data = '\n'.join(vim.current.buffer)
    newline = utils.get_super(data, row, True)
    vim.current.buffer[row - 1:] = [newline] + vim.current.buffer[row - 1:]

