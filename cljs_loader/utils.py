def to_tag(bundle):
    return \
        '<script src="{}"></script>' \
        '<script>window.onload = function () {{ {} }}</script>' \
        .format(bundle['url'], bundle['on-jsload'])
