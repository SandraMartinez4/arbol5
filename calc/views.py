from django.shortcuts import render
from dataclasses import dataclass
import ast

# Nodo del árbol
@dataclass
class ExprNode:
    op: str = None
    left: 'ExprNode' = None
    right: 'ExprNode' = None
    value: float = None
    name: str = None

    def eval(self, env):
        if self.op == 'const':
            return self.value
        if self.op == 'var':
            return float(env[self.name])
        l = self.left.eval(env) if self.left else None
        r = self.right.eval(env) if self.right else None
        if self.op == '+': return l + r
        if self.op == '-': return l - r
        if self.op == '*': return l * r
        if self.op == '/': return l / r
        if self.op == '**': return l ** r
        if self.op == 'neg': return -r
        raise ValueError('Operación no soportada: ' + str(self.op))

# Convierte un AST de Python limitado a un ExprNode.
ALLOWED_OPS = {
    ast.Add: '+', ast.Sub: '-', ast.Mult: '*', ast.Div: '/', ast.Pow: '**'
}

def ast_to_exprnode(node):
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in ALLOWED_OPS:
            raise ValueError('Operador no permitido')
        left = ast_to_exprnode(node.left)
        right = ast_to_exprnode(node.right)
        return ExprNode(op=ALLOWED_OPS[op_type], left=left, right=right)
    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.USub):
            operand = ast_to_exprnode(node.operand)
            return ExprNode(op='neg', right=operand)
        raise ValueError('Unary op no permitido')
    if isinstance(node, ast.Num):  # Python <3.8
        return ExprNode(op='const', value=node.n)
    if isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return ExprNode(op='const', value=node.value)
        raise ValueError('Solo números permitidos como constantes')
    if isinstance(node, ast.Name):
        if node.id in ('X', 'Y'):
            return ExprNode(op='var', name=node.id)
        raise ValueError('Solo variables permitidas: X y Y')
    if isinstance(node, ast.Expr):
        return ast_to_exprnode(node.value)
    raise ValueError('Nodo AST no soportado: ' + node.__class__.__name__)

def parse_expr(text):
    """Parsea una expresión segura (solo operadores permitidos y nombres X/Y)."""
    if not text:
        raise ValueError('Expresión vacía')
    parsed = ast.parse(text, mode='eval')
    return ast_to_exprnode(parsed.body)

# Creamos árboles por defecto
def default_trees():
    tree1 = parse_expr('X**2')
    tree2 = parse_expr('2*Y')
    return tree1, tree2

def input_view(request):
    return render(request, 'calc/form.html')

def result_view(request):
    X = request.POST.get('X') or request.GET.get('X', '')
    Y = request.POST.get('Y') or request.GET.get('Y', '')
    expr1 = request.POST.get('expr1') or request.GET.get('expr1', '').strip()
    expr2 = request.POST.get('expr2') or request.GET.get('expr2', '').strip()

    error = None
    results = []
    # valores por defecto para expresiones si quedaron vacías
    if expr1 == '':
        expr1 = 'X**2'
    if expr2 == '':
        expr2 = '2*Y'

    try:
        env = {'X': float(X), 'Y': float(Y)}
    except Exception:
        error = 'Introduce valores numéricos para X y Y.'
        return render(request, 'calc/result.html', {'X': X, 'Y': Y, 'results': results, 'error': error})

    try:
        tree1 = parse_expr(expr1)
        tree2 = parse_expr(expr2)
        val1 = tree1.eval(env)
        val2 = tree2.eval(env)
        results = [val1, val2]
    except Exception as e:
        error = f'Error al evaluar expresiones: {e}'

    return render(request, 'calc/result.html', {
        'X': X, 'Y': Y, 'expr1': expr1, 'expr2': expr2, 'results': results, 'error': error
    })
