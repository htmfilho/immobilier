##############################################################################
#
#    Immobilier it's an application
#    designed to manage the core business of property management, buildings,
#    rental agreement and so on.
#
#    Copyright (C) 2016-2018 Verpoorten Leïla
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
A = "A <= 50 kwh/m².an"
B = "B 51>= <90 kwh/m².an"
C = "C 91>= <150 kwh/m².an"
D = "D 151>= <230 kwh/m².an"
E = "E 231>= <330 kwh/m².an"
F = "F 331>= <450 kwh/m².an"
G = "G >450 kwh/m².an"

PERFORMANCE_ENERGETIQUES = (
    (A, A),
    (B, B),
    (C, C),
    (D, D),
    (E, E),
    (F, F),
    (G, G),
)
