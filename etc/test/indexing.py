indexing_tests = [
    "a.b()",
    "a.b.c()",
    "a().b.c",
    "a.b().c",
    "a.b().c()",
    "a().b.c()",

    "a.b(1, 2, z)",
    "a.b.c()",
    "a().b.c",
    "a.b().c",
    "a.b().c()",
    "a(x, y).b.c(1, 2)",
]