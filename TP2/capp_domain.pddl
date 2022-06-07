(define (domain capp)
(:requirements :equality :strips)
(:predicates
    
    (lado ?l)
    (tipo ?t)
    (altura ?al)
    (feature ?f)
	(herramienta ?h)
    (orientacion ?o)
    (operacion ?oper)
    
    
    (lado-pieza ?lp)
    (orientacion-pieza ?op)

    (herramienta-actual ?ha)
    (herramienta-altura ?al)
    

    (lado-feature ?f ?l)
    (altura-feature ?f ?al)
    (orientacion-feature ?f ?o)
    (feature-tipo ?f ?feat-tipo)

    (fabricable ?t ?oper)
    (herramienta-necesaria ?h ?oper)

    (fabricada ?feat)

) 

(:action orientar-pieza
 :parameters ( ?orientacion-inicial ?orientacion-final )
 :precondition
	(and 
        (orientacion-pieza ?orientacion-inicial)  
        (orientacion ?orientacion-inicial) 
        (orientacion ?orientacion-final)
    )
 :effect
	(and 
		(orientacion-pieza ?orientacion-final)
		(not (orientacion-pieza ?orientacion-inicial))
	)
)

(:action mover-pieza
 :parameters ( ?lado-inicial ?lado-final )
 :precondition
	(and 
        (lado-pieza ?lado-inicial)  
        (lado ?lado-inicial) 
        (lado ?lado-final)
    )
 :effect
	(and 
		(lado-pieza ?lado-final)
		(not (lado-pieza ?lado-inicial))
	)
)

(:action cambiar-herramienta
 :parameters ( ?herramienta-inicial ?herramienta-final )
 :precondition
	(and 
        (herramienta-actual ?herramienta-inicial)  
        (herramienta ?herramienta-inicial) 
        (herramienta ?herramienta-final)
    )
 :effect
	(and 
		(herramienta-actual ?herramienta-final)
		(not (herramienta-actual ?herramienta-inicial))
	)
)

(:action mover-herramienta
 :parameters ( ?altura-inicial ?altura-final )
 :precondition
	(and 
        (herramienta-altura ?altura-inicial)  
        (altura ?altura-inicial) 
        (altura ?altura-final)
    )
 :effect
	(and 
		(herramienta-altura ?altura-final)
		(not (herramienta-altura ?altura-inicial))
	)
)

(:action maquinado
 :parameters ( ?o ?f ?t ?oper ?h ?al)
 :precondition
	(and 
        (operacion ?oper)
        (orientacion ?o) 
        (herramienta ?h)
        (feature ?f)
        (tipo ?t)

        (herramienta-actual ?h)
        (herramienta-altura ?al)
        (orientacion-pieza ?o)
        (feature-tipo ?f ?t)
        (fabricable ?t ?oper)
        (herramienta-necesaria ?h ?oper)
        (orientacion-feature ?f ?o)
        (altura-feature ?f ?al)
        
    )
 :effect
    (fabricada ?f)
)
)
