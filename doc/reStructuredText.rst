**************************
reStructuredText Tutorial!
**************************

Ce chapitre est une introduction à :strong:`reStructuredText`, le markup
language utilisé par :strong:`Sphinx`.

Les paragraphes
===============

Ceci est un paragraphe ! Il est délimité par un ou plusieurs saut de ligne,
chaque nouvelle ligne doit être indentée comme les précédentes.
On ne peux pas "revenir à la ligne" dans un paragraphe, c'est la plus petite
"unité d'organisation" du texte.

Inline markup
=============

Dans un paragraphe on peut écrire des trucs en *italique*, en **gras** ou en
police ``monospaced`` (pour afficher du code par exemple) en encadrant le texte
avec, respectivement, une étoile, deux étoiles ou des backquotes.
Si on veux inclure des étoiles (*) dans un texte en *italique* ou en **gras**,
il faut les précéder d'un backslash (\\). Il en est de même pour les backquotes
dans un text en police ``monospaced``.

* :literal:`*Une étoile*`: *Une étoile*
* :literal:`**Deux étoiles**`: **Deux étoiles**
* :literal:`\`\`Deux backquotes\`\``: ``Deux backquotes``

Les listes
==========

On peux faire plusieurs types de listes dont les listes normales et les listes
numérotées, les listes de définitions et les listes à champs. Pour faire des
listes simples, il suffit de précéder un paragraphe d'une étoile. Pour les
listes numérotées, on précède le paragraphe d'un nombre suivi d'un point si on
souhaite numéroter les parties manuellement ou d'un dièse (#) suivi d'un point
si on veut que :strong:`Sphinx` numérote la liste automatiquement. Pour les
autres listes c'est un peu plus compliqué.

Listes simples
--------------

Voici un exemple de liste simple::

    * Ceci est le premier élément de ma liste
    * Voici le second
        * Voici un élément intermédiaire histoire de montrer qu'on peut faire
          des sous-listes
    * Un troisième qui prend deux
      lignes pour rien (notez l'indentation...)

Ce qui donne:

* Ceci est le premier élément de ma liste
* Voici le second
    * Voici un élément intermédiaire histoire de montrer qu'on peut faire des
      sous-listes
* Un troisième qui prend deux
  lignes pour rien (notez l'indentation...)

Listes numérotées
-----------------

Voici un exemple de liste numérotée::

    1. Ceci est mon premier élément
        1.1. Ceci est mon premier sous élément
    2. Ceci est mon deuxième élément
    3. Ceci est mon troisième élément

Qui donne le texte suivant une fois générée:

1. Ceci est mon premier élément
    1.1. Ceci est mon premier sous élément
2. Ceci est mon deuxième élément
3. Ceci est mon troisième élément

Listes auto-numérotées
----------------------

Voici un exemple de super liste auto-numérotées que vazy elles sont trop bien::

    #. Ceci est mon premier élément
    #. Ceci est mon second élément, plus original que le précédent...
    #. Ceci est mon DERNIER élément

Voici le rendu:

#. Ceci est mon premier élément
#. Ceci est mon second élément, plus original que le précédent...
#. Ceci est mon DERNIER élément

Petit bémol, on ne peux pas faire de sous élément qui se numérotent tout seul.

Listes de définitions
---------------------

Sait on jamais, ca pourrait servir. Ce sont des listes avec un terme qui fait
maximum une ligne, suivi de sa définition::

    Loutre
        Animal qu'il est trop mignon
    Poney
        Animal qu'il est trop gentil

Et voilà le résultat (non, ce n'est pas évident mais c'est bien d'une liste):

Loutre
    Animal qu'il est trop mignon
Poney
    Animal qu'il est trop gentil

Les listes des champs
---------------------

Alors, ci dessous un exemple de ce qu'on appelle des "field-lists", qui sont
utile pour la documentation du code, histoire de passer des informations à
:strong:`Sphinx` depuis les docstrings::

    :MonChamp: Est pas très grand
    :Toto: * Est pas drôle
           * Mange de la salade
    :Titi: Est une fille

Ce qui produit un résultat pas très éthétique, mais c'est surtout utile pour
déplacer la doc dans le code, comme dit plus haut.

:MonChamp: Est pas très grand
:Toto: * Est pas drôle
       * Mange de la salade
:Titi: Est une fille

Les blocs de code
=================

Je suis sur que vous vous demandez tous comment je fais pour vous montrer le
code source de la page dans les exemples ! (Oué non en fait j'y crois pas trop
mais on va faire comme si). Et bien c'est très simple ! Il suffit de précéder
du texte par "::" suivis d'un saut de ligne ! C'est pas très clair ? Voici un
exemple qui va montrer comment je fais les exemples (Youhou!)::

    Youpi je suis une paragraphe décrivant un truc trop cool que je veux
    absolument montrer mais sous forme littérale:

    ::

        if __name__ == '__main__':
            print("Poney!")

Et ci dessous admirrez le rendu, avec des couleurs itout itout grâce à
:strong:`Pygments`:

Youpi je suis une paragraphe décrivant un truc trop cool que je veux
absolument montrer mais sous forme littérale:

::

    if __name__ == '__main__':
        print("Poney!")

Petit conus pour les mecs qui aiment en faire le moins possible, il y a trois
manière d'introduire un bloc de code qui donnent exactement le même rendu, mais
en demandant plus ou moins d'effort de votre part::

    Paragraphe:
    
    ::

        Code

    Paragraphe: ::

        Code

    Paragraphe::

        Code

Voilà, ces trois formes donnent exactement la même chose au final, c'est à dire
un paragraphe suivis de ':' puis le bloc littéral en dessous.

Les bloc "Doctest"
==================

Vu qu'on vient de voir comment faire des blocs de texte non intérprété par
:strong:`Sphinx`, on va jeter un coup d'oeil au bloc :emphasis:`Doctest`. Ces
blocs sont plutôt intéressants puisqu'ils vont nous permettre de tester nos
fonctions via un module de :strong:`Sphinx` (sphinx.ext.doctest). C'est bien
pratique car ca permet de garder les tests unitaires dans les docstrings des
fonctions, et en plus ca fait genre on fait du TDD et tout. Voici la syntaxe::

    >>> print("LOOTRE!")
    LOOTRE!

Voilà, rien de bien compliqué la dedans, et on peut également l'utiliser pour
documenter si on veux montrer un exemple dans une session intéractive Python,
et ce qui est fun c'est que je n'ai pas besoin de vous montrer le rendu puisque
c'est le même que dans l'exemple du dessus. Bon, juste histoire de vous le
prouver:

>>> print("LOOTRE!")
LOOTRE!

Les liens
=========

Attention, petite partie vraiment intéressante... Voici comment on créé un
`lien <http://upload.wikimedia.org/wikipedia/commons/d/db/Otter_in_winter.jpg>`_::

        Voici un lien vers `Google <http://www.google.com>`_ !

Oui, il faut bien le '_' après le lien, ce n'est pas une erreur.

Les titres
==========

Voici comment on met en évidence un titre en suivant les conventions de la doc
Python::

        ==========
        H1 - Parts
        ==========

        *************
        H2 - Chapters
        *************

        H3 - Sections
        =============

        H4 - Subsections
        ----------------

        H5 - Subsubsections
        ^^^^^^^^^^^^^^^^^^^

        H6 - Paragraphs
        """""""""""""""

Pour le titre du tutoriel j'ai utilisé la syntaxe H2 par exemple car il n'est
composé que d'un seul chapitre avec plein de sections.

Les commentaires
================

Car ca peut être utile quelques fois de commenter la source de la documentation
voici comment écrire un commentaire::

        .. Ceci est un commentaire sur une ligne

        ..

            Ceci est un commentaire qui s'étend sur plusieurs lignes et occupe
            pas mal de place dans la source
