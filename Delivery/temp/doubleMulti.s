	.section	__TEXT,__text,regular,pure_instructions
	.macosx_version_min 10, 10
	.section	__TEXT,__literal8,8byte_literals
	.align	3
LCPI0_0:
	.quad	4614256656552045848     ## double 3.1415926535897931
LCPI0_1:
	.quad	4621745711392638430     ## double 9.869604401089358
	.section	__TEXT,__text,regular,pure_instructions
	.globl	_main
	.align	4, 0x90
_main:                                  ## @main
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp0:
	.cfi_def_cfa_offset 16
Ltmp1:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp2:
	.cfi_def_cfa_register %rbp
	leaq	L_.str(%rip), %rdi
	movsd	LCPI0_0(%rip), %xmm0
	movb	$1, %al
	callq	_printf
	leaq	L_.str1(%rip), %rdi
	movb	$1, %al
	movsd	LCPI0_0(%rip), %xmm0
	callq	_printf
	leaq	L_.str2(%rip), %rdi
	movsd	LCPI0_1(%rip), %xmm0
	movb	$1, %al
	callq	_printf
	xorl	%eax, %eax
	popq	%rbp
	retq
	.cfi_endproc

	.section	__TEXT,__cstring,cstring_literals
L_.str:                                 ## @.str
	.asciz	"X1: %.100f.\n"

L_.str1:                                ## @.str1
	.asciz	"X2: %.100f.\n"

L_.str2:                                ## @.str2
	.asciz	"DoubleMulti: %.100f.\n"


.subsections_via_symbols
