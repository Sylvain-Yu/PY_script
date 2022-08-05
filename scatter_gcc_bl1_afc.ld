MEMORY
{
    INTFLASH (rx) : ORIGIN = (0x00000000), LENGTH = (2048*1024)
	INTRAM (rwx) : ORIGIN = (0x10000000), LENGTH = (16*1024)
    STACK (rwx) : ORIGIN = (0x70000000)+((32*1024)+(31*1024)), LENGTH = 1024
    DPRAM_FLU (rwx) : ORIGIN = (0x60000000), LENGTH = ((8*1024))
}
SECTIONS
{
    .afc :
	{
		_afc = .;
		KEEP(*csp_flash_ctrl.o(.text .text*))
		KEEP(*bsp_flash.o(.text .text*))
		KEEP(*flash_ctrl_routine.o(.text .text*))
		. = ALIGN(32);
		_eafc = .;
	} >INTRAM
	.text : AT ((0x00000000))
    {
        _text = .;
        KEEP(*(.VECTORS))
		*(.text*)
	   *(EXCLUDE_FILE(*csp_flash_ctrl.o) .text .text*)
	   *(EXCLUDE_FILE(*bsp_flash.o) .text .text*)
	   *(EXCLUDE_FILE(*flash_ctrl_routine.o) .text .text*)
       *(.rodata)
       *(.rodata*)
       *(.glue_7)
       *(.glue_7t)
    } > INTFLASH
    .ARM.exidx :
    {
        *(.ARM.exidx* .gnu.armexidx.*)
        . = ALIGN(4);
        _endcode = .;
    } > INTFLASH
	
   .ram :
    {
        _ram = .;
		_data = .;
       *(.data)
       *(.data*)
        . = ALIGN(32);
        _edata = .;
    } > INTRAM AT>INTFLASH
    .bss :
    {
        _bss = .;
       *(.bss)
       *(.bss*)
        *(COMMON)
        . = ALIGN(32);
        _ebss = .;
        PROVIDE ( end = . );
    	PROVIDE ( _end = . );
    } > INTRAM
    .stack :
    {
        _stacktop = .;
    } >STACK
    .dpram_flu :
    {
        _dpram_flu = .;
    } > DPRAM_FLU
}
