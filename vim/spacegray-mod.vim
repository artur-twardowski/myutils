" Spacegray-mod.vim -- Vim colorscheme
" Maintainer: Akshay Hegde (github.com/ajh17)
" Version: 1.5
" Description: A colorscheme loosely modeled after the spacegray theme for Xcode
" Note: This colorscheme is 256color and up only
" Last Change: 2020 Dec 23

" Setup {{{1
hi clear

if has('gui_running') && &background !=# 'dark'
  set background=dark
endif

if exists('syntax_on')
  syntax reset
endif

" Options {{{1

let g:colors_name = 'spacegray-mod'

" Colorscheme definitions {{{1
hi Normal        ctermbg=233  ctermfg=247    guibg=#111314  guifg=#939393  cterm=NONE      gui=NONE

hi Comment       ctermbg=NONE ctermfg=240    guibg=NONE     guifg=#585858  cterm=NONE      gui=NONE

hi Conceal         ctermbg=NONE ctermfg=250    guibg=NONE     guifg=#B3B8C4  cterm=NONE      gui=NONE
hi NonText         ctermbg=NONE ctermfg=8      guibg=NONE     guifg=#3E4853  cterm=NONE      gui=NONE
hi Title           ctermbg=NONE ctermfg=250    guibg=NONE     guifg=#B3B8C4  cterm=bold      gui=bold
hi Constant        ctermbg=NONE ctermfg=130    guibg=NONE     guifg=#C5735E  cterm=NONE      gui=NONE
hi Function        ctermbg=NONE ctermfg=118    guibg=NONE     guifg=#5fafff  cterm=NONE      gui=NONE
hi Identifier      ctermbg=NONE ctermfg=179    guibg=NONE     guifg=#E5C0F8  cterm=NONE      gui=NONE
hi PreProc         ctermbg=NONE ctermfg=153    guibg=NONE     guifg=#afd7ff  cterm=NONE      gui=NONE
hi Special         ctermbg=NONE ctermfg=103    guibg=NONE     guifg=#7D8FA3  cterm=NONE      gui=NONE
hi SpecialKey      ctermbg=NONE ctermfg=59     guibg=NONE     guifg=#4C5966  cterm=NONE      gui=NONE
hi SpecialComment  ctermbg=NONE ctermfg=242    guibg=NONE     guifg=#657785  cterm=bold      gui=bold
hi Statement       ctermbg=NONE ctermfg=254    guibg=NONE     guifg=#e4e4e4  cterm=bold      gui=bold
hi String          ctermbg=NONE ctermfg=153    guibg=NONE     guifg=#afd7ff  cterm=NONE      gui=NONE
hi Type            ctermbg=NONE ctermfg=220    guibg=NONE     guifg=#dfc820  cterm=NONE      gui=NONE

hi Cursor          ctermbg=fg   ctermfg=bg     guibg=fg       guifg=bg       cterm=NONE      gui=NONE
hi CursorColumn    ctermbg=0    ctermfg=NONE   guibg=#303030  guifg=NONE     cterm=NONE      gui=NONE
hi CursorLine      ctermbg=0    ctermfg=NONE   guibg=#2f1000  guifg=NONE     cterm=NONE      gui=NONE
hi ColorColumn     ctermbg=235  ctermfg=NONE   guibg=#303537  guifg=NONE     cterm=NONE      gui=NONE
hi SignColumn      ctermbg=233  ctermfg=250    guibg=#141617  guifg=#B3B8C4  cterm=NONE      gui=NONE

hi Todo            ctermbg=NONE ctermfg=NONE   guibg=NONE     guifg=NONE     cterm=reverse   gui=reverse
hi Error           ctermbg=52   ctermfg=12     guibg=NONE     guifg=#AF5F5F  cterm=underline gui=reverse
hi ErrorMsg        ctermbg=NONE ctermfg=9      guibg=NONE     guifg=#C5735E  cterm=NONE      gui=NONE
hi Question        ctermbg=NONE ctermfg=214    guibg=NONE     guifg=#FFAF00  cterm=NONE      gui=NONE
hi ModeMsg         ctermbg=NONE ctermfg=249    guibg=NONE     guifg=#808080  cterm=NONE      gui=NONE
hi MoreMsg         ctermbg=NONE ctermfg=249    guibg=NONE     guifg=#808080  cterm=NONE      gui=NONE
hi WarningMsg      ctermbg=NONE ctermfg=12     guibg=NONE     guifg=#7D8FA3  cterm=NONE      gui=NONE

hi DiffAdd         ctermbg=65   ctermfg=232    guibg=#5F875F  guifg=#080808  cterm=NONE      gui=NONE
hi DiffChange      ctermbg=237  ctermfg=NONE   guibg=#3A3A3A  guifg=NONE     cterm=NONE      gui=NONE
hi DiffDelete      ctermbg=234  ctermfg=9      guibg=NONE     guifg=#CC6666  cterm=NONE      gui=NONE
hi DiffText        ctermbg=60   ctermfg=251    guibg=#5F5F87   guifg=#D0D0D0 cterm=NONE      gui=NONE

hi helpLeadBlank   ctermbg=NONE ctermfg=NONE   guibg=NONE     guifg=NONE     cterm=NONE      gui=NONE
hi helpNormal      ctermbg=NONE ctermfg=NONE   guibg=NONE     guifg=NONE     cterm=NONE      gui=NONE

hi LineNr          ctermbg=NONE ctermfg=88     guibg=#111314  guifg=#870000  cterm=NONE      gui=NONE
hi CursorLineNr    ctermbg=NONE ctermfg=196    guibg=NONE     guifg=#ff0000  cterm=NONE      gui=NONE

hi Pmenu           ctermbg=246  ctermfg=0      guibg=#949494  guifg=#000000  cterm=NONE      gui=NONE
hi PmenuSel        ctermbg=234  ctermfg=196    guibg=#252525  guifg=#FF2A1F  cterm=bold      gui=bold
hi PmenuSbar       ctermbg=233  ctermfg=000    guibg=#333233  guifg=#000000  cterm=NONE      gui=none
hi PmenuThumb      ctermbg=235  ctermfg=137    guibg=NONE     guifg=#171717  cterm=none      gui=none

hi WildMenu        ctermbg=110  ctermfg=235    guibg=#8FAFD7  guifg=#141617  cterm=bold      gui=bold

hi StatusLine         ctermbg=235 ctermfg=249 guibg=#303537 guifg=#B3B8C4 cterm=NONE   gui=NONE
hi StatusLineTerm     ctermbg=235 ctermfg=249 guibg=#303537 guifg=#B3B8C4 cterm=NONE   gui=NONE
hi TablineSel         ctermbg=235 ctermfg=249 guibg=#303537 guifg=#B3B8C4 cterm=NONE   gui=NONE
hi TablineFill        ctermbg=235 ctermfg=249 guibg=#303537 guifg=#B3B8C4 cterm=NONE   gui=NONE
hi StatusLineNC     ctermbg=237 ctermfg=0 guibg=#3a3a3a guifg=#949494 cterm=NONE   gui=NONE
hi StatusLineTermNC ctermbg=237 ctermfg=0 guibg=#3a3a3a guifg=#949494 cterm=NONE   gui=NONE
hi Tabline          ctermbg=232 ctermfg=239 guibg=#1C1F20 guifg=#7C7F88 cterm=NONE   gui=NONE

hi Underlined      ctermbg=NONE ctermfg=66     guibg=NONE     guifg=#5F8787  cterm=NONE      gui=NONE
hi Ignore          ctermbg=NONE ctermfg=250    guibg=NONE     guifg=#BCBCBC  cterm=NONE      gui=NONE

hi Visual          ctermbg=233  ctermfg=4      guibg=#111314  guifg=#6E9CAF  cterm=reverse   gui=reverse
hi VisualNOS       ctermbg=8    ctermfg=NONE   guibg=NONE     guifg=NONE     cterm=bold      gui=bold

hi FoldColumn      ctermbg=NONE ctermfg=242    guibg=#1C1C1C  guifg=#6C6C6C  cterm=NONE      gui=NONE
hi Folded          ctermbg=NONE ctermfg=242    guibg=#1C1C1C  guifg=#6C6C6C  cterm=NONE      gui=NONE

hi VertSplit       ctermbg=237 ctermfg=238   guibg=#3a3a3a  guifg=#444444  cterm=NONE      gui=NONE

hi IncSearch       ctermbg=9    ctermfg=0      guibg=#AF5F5F  guifg=#141617  cterm=NONE      gui=NONE
hi Search        ctermbg=2    ctermfg=232    guibg=#919652  guifg=#141617  cterm=NONE      gui=NONE

hi Directory       ctermbg=NONE ctermfg=24     guibg=NONE     guifg=#5FAFAF  cterm=NONE      gui=NONE
hi MatchParen      ctermbg=NONE ctermfg=11     guibg=NONE     guifg=#E5C078  cterm=bold      gui=bold

hi SpellBad        ctermbg=52   ctermfg=9      guibg=#5F0000  guifg=#CC6666  cterm=NONE      gui=NONE
hi SpellRare       ctermbg=53   ctermfg=13     guibg=#5F005F  guifg=#B294BB  cterm=NONE      gui=NONE
hi SpellCap        ctermbg=17   ctermfg=12     guibg=#00005F  guifg=#81A2BE  cterm=NONE      gui=NONE
hi SpellLocal      ctermbg=24   ctermfg=14     guibg=#005F5F  guifg=#8ABEB7  cterm=NONE      gui=NONE

" Highlights {{{1
hi link Boolean             Constant
hi link Character           Constant
hi link Number              Constant

hi link Float               Number

hi link Define              Preproc
hi link Include             Preproc
hi link Macro               Preproc
hi link PreCondit           PreProc

hi link Conditional         Statement
hi link Exception           Statement
hi link HelpCommand         Statement
hi link HelpExample         Statement
hi link Keyword             Statement
hi link Label               Statement
hi link Operator            Statement
hi link Repeat              Statement

hi link StorageClass        Type
hi link Structure           Type
hi link Typedef             Type

hi link Debug               Special
hi link Delimiter           Special
hi link SpecialChar         Special
hi link Tag                 Special

hi link Terminal            Normal

" HTML
hi link htmlEndTag          htmlTagName
hi link htmlLink            Function
hi link htmlSpecialTagName  htmlTagName
hi link htmlTag             htmlTagName

" Rails
hi link rubyRailsARAssociationMethod  Statement
hi link rubyRailsARValidationMethod   Statement
hi link rubyRailsARMethod             Statement
hi link rubyRailsARCallbackMethod     Statement
hi link rubyRailsARClassMethod        Statement

" Diff
hi link diffAdded           String
hi link diffRemoved         Function

hi GitGutterAdd  guifg=#009900 ctermfg=2
hi GitGutterChange guifg=#bbbb00 ctermfg=3
hi GitGutterDelete guifg=#ff2222 ctermfg=1

if (has('terminal') && has('termguicolors')) || has('gui_running')
  let g:terminal_ansi_colors = [
        \ '#3A3E42',
        \ '#BF6262',
        \ '#A2A565',
        \ '#E9A96F',
        \ '#789BAD',
        \ '#9F7AA5',
        \ '#638E8A',
        \ '#737673',
        \ '#5D6369',
        \ '#BF6262',
        \ '#A5A76E',
        \ '#E9A96F',
        \ '#789BAD',
        \ '#9F7AA5',
        \ '#9F7AA5',
        \ '#E3E8E3'
        \ ]
endif
