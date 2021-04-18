#!/usr/bin/python

import sys


def define_visitor(file, base_name, types):
    file.write("    interface Visitor<R> {\n");

    for node_type in types:
        type_name = node_type.split(':')[0].strip()
        file.write("        R visit" + type_name + base_name + "(" + type_name +
                   " " + base_name.lower() + ");\n");

    file.write("    }\n");


def define_type(file, base_name, class_name, field_list):
    # Class header
    file.write("    static class " + class_name + " extends " + base_name + " {\n")

    # Fields
    fields = field_list.split(", ")
    for field in fields:
        file.write("        final " + field + ";\n")
    file.write('\n')

    # Constructor
    file.write("        " + class_name + "(" + field_list + ") {\n")

    # Parameters
    for field in fields:
        name = field.split(" ")[1]
        file.write("            this." + name + " = " + name + ";\n")
    file.write("        }\n")

    file.write('\n')
    file.write("        @Override\n")
    file.write("        <R> R accept(Visitor<R> visitor) {\n")
    file.write("            return visitor.visit" +
               class_name + base_name + "(this);\n")
    file.write("        }\n")


    file.write("    }\n")



def define_ast(output_dir, base_name, types):
    path = output_dir + '/' + base_name + '.java'
    with open(path, 'w') as file:
        file.write("package jlox;\n")
        file.write("\n")
        file.write("import java.util.List;\n")
        file.write("\n")
        file.write("abstract class " + base_name + " {\n")
        define_visitor(file, base_name, types)
        file.write('\n')

        # Ast classes
        for node_type in types:
            class_name = node_type.split(":")[0].strip()
            fields = node_type.split(":")[1].strip()
            define_type(file, base_name, class_name, fields)
            file.write('\n')

        file.write("    abstract <R> R accept(Visitor<R> visitor);\n")

        file.write("}\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: generate_ast <output directory>")
        sys.exit(64)

    output_dir = sys.argv[1]

    define_ast(output_dir, "Expr", [
        "Binary   : Expr left, Token operator, Expr right",
        "Grouping : Expr expression",
        "Literal  : Object value",
        "Unary    : Token operator, Expr right",
    ])
