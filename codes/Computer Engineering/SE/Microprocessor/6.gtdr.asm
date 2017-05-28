/*
Write X86/64 ALP to switch from real mode to protected mode and display the values of
GDTR, LDTR, IDTR, TR and MSW Registers.
*/
%macro scall 4
	mov rax,%1
	mov rdi,%2
	mov rsi,%3
	mov rdx,%4
	syscall
%endmacro

section .data
	realmsg db 10,"Processor is in REAL MODE!"
	rl equ $-realmsg
	
	promsg db 10,"Processor is in PROTECTED MODE!"
	pl equ $-promsg
	
	gdtmsg db 10,"Contents of GDT => "
	l1 equ $-gdtmsg
	
	ldtmsg db 10,"Contents of LDT => "
	l2 equ $-ldtmsg
	
	idtmsg db 10,"Contents of IDT => "
	l3 equ $-idtmsg
	
	trmsg db 10,"Contents of TR => "
	l4 equ $-trmsg
	
	mswmsg db 10,"Contents of MSW => "
	l5 equ $-mswmsg
	
	colon db " : "
	colon_len equ $-colon
	
section .bss
	cr0_data resd 1
	GDT resd 1
		resw 1
	LDT resw 1
	IDT resd 1
		resw 1
	TR resw 1
	dispbuff resb 2
	
	
section .text
	global _start
	
_start:
	smsw eax
	
	mov [cr0_data],eax
	
	shr eax,1
	jc pro
	scall 1,1,realmsg,rl
	jmp below
	
	pro:
		scall 1,1,promsg,pl
		
	below:
		sgdt [GDT]
		sldt [LDT]
		str [TR]
		sidt [IDT]
		
		scall 1,1,gdtmsg,l1
		mov bx,[GDT+4]
		call display
		mov bx,[GDT+2]
		call display
		scall 1,1,colon,colon_len
		mov bx,[GDT]
		call display

		scall 1,1,ldtmsg,l2
		mov bx,[LDT]
		call display

		scall 1,1,idtmsg,l3
		mov bx,[IDT+4]
		call display
		mov bx,[IDT+2]
		call display
		scall 1,1,colon,colon_len
		mov bx,[IDT]
		call display
		
		scall 1,1,trmsg,l4
		mov bx,[TR]
		call display
	
		scall 1,1,mswmsg,l5
		mov bx,[cr0_data+2]
		call display
		mov bx,[cr0_data]
		call display

		
				
		exit:
			scall 60,0,0,0
		
;**************DISPLAY Procedure************
display:
	mov rsi,dispbuff
	mov rcx,4
	
	bck:
		rol bx,4
		mov al,bl
		and al,0fh
		cmp al,09h
		jbe nxt
		add al,07h
		
		nxt:
			add al,30h
			mov [rsi],al
			inc rsi
			dec rcx
			jnz bck
			
		scall 1,1,dispbuff,4
			
		ret
