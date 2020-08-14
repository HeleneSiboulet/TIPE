(TeX-add-style-hook "200813-TIPE-SibouletH"
 (lambda ()
    (LaTeX-add-bibliographies
     "/Users/siboulet/Desktop/bibH")
    (LaTeX-add-labels
     "fig:190101Lolita"
     "MonTableau")
    (TeX-add-symbols
     '("sub" 1)
     '("addref" 1)
     '("comment" 1)
     '("doi" 1)
     '("mycommand" 1)
     "Angstrom")
    (TeX-run-style-hooks
     "listings"
     "scrpage2"
     "automark"
     "framed"
     "sectsty"
     "xcolor"
     "dvipsnames"
     "caption"
     "array"
     "rotating"
     "float"
     "pbox"
     "multicol"
     "multirow"
     "longtable"
     "threeparttable"
     "booktabs"
     "epstopdf"
     "tabularx"
     "geometry"
     "graphicx"
     "makeidx"
     "amssymb"
     "amsfonts"
     "amsmath"
     "fontenc"
     "T1"
     "inputenc"
     "utf8"
     "babel"
     "francais"
     "latex2e"
     "art11"
     "article"
     "11pt"
     "a4paper")))

