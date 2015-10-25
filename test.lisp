(ql:quickload :alexandria)
(ql:quickload :split-sequence)
(ql:quickload :anaphora)

; Debugging-stuff
(let (hmph)
  (defun set-hmph (v) (setf hmph v))
  (defun get-hmph () hmph))

(defconstant jstring (jclass "java.lang.String"))
(defconstant jobject (jclass "java.lang.Object"))
(defconstant jdouble (jclass "java.lang.Double"))
(defconstant jinteger (jclass "java.lang.Integer"))

(defmacro new-array ((type) &rest values)
  `(mnew-jarray ,type ,@values))

(defmacro defparameters (&rest definitions)
  (list* 'progn (loop for def in definitions
                      collect `(defparameter ,@def))))

(defun mnew-jarray (type &rest values)
  (let ((arr (jnew-array (jclass "java.lang.String") (length values))))
    (prog1 arr
      (loop for i from 0
            for item in values
            do (setf (jarray-ref arr i) item)))))

(defun symbol-to-java-string (sym)
  (etypecase sym
    (string sym)
    (symbol (flet ((splitter (s) (split-sequence:split-sequence #\- s)))
              (let* ((name (symbol-name sym))
                     (split-name (loop for item in (splitter name)
                                       collect (string-downcase item)))
                     (capitalized (loop for item in split-name
                                        collect (string-capitalize item)))
                     (java-name (cons (car split-name)
                                      (cdr capitalized)))
                     (result (apply #'concatenate (cons 'string java-name))))
                result)))))

(defmacro call-t (instance &body methods)
  (alexandria:once-only (instance)
    `(macrolet ((-> (method &rest args)
                  `(jcall ,(symbol-to-java-string method)
                          ,',instance
                          ,@args)))
       ,@methods)))

(defmacro call (instance &body methods)
  (alexandria:once-only (instance)
    (list* 'progn
           (loop for invocation in methods
                 collect (destructuring-bind (method &rest args) invocation
                           `(jcall ,(symbol-to-java-string method) ,instance ,@args))))))

(defmacro call-1 (instance method &rest args)
  `(call ,instance (,method ,@args)))

(defmacro thread (inst &rest args)
  (alexandria:once-only (inst)
    (list 'let* (loop for arg in args
                      collect (destructuring-bind (method &rest args) arg
                                `(,inst (,method ,inst ,@args))))
          inst)))

(defun iterable-to-list (iterable)
  (let ((iterator (call-1 iterable iterator)))
    (call-t iterator
      (loop while (-> has-next)
            collect (-> next)))))

(defun object-to-string (obj)
  (call-1 obj to-string))


(defconstant start (get-internal-run-time))
(defparameter *args* (new-array (jstring) "--graphs" "." "--router" "portland"))
(defconstant otps-entry-point (jclass "org.opentripplanner.scripting.api.OtpsEntryPoint"))
; Find a better way to call fromArgs . . . 
(defparameter *otp* (jstatic (aref (jclass-methods otps-entry-point) 1) nil *args*))

(call-t *otp*
  (defparameters (*router* (-> get-router "portland"))
                 (*req*    (-> create-request)))

  (defparameters (*points* (-> load-c-s-v-population "points.csv" "Y" "X"))
                 (*dests*  (-> load-c-s-v-population "points.csv" "Y" "X"))

                 (*matrix-csv* (-> "createCSVOutput"))))

(call *req*
  (set-date-time 2015 9 15 10 0 0)
  (set-max-time-sec 7200)
  (set-modes "WALK,BUS,RAIL"))

(call-1 *matrix-csv* set-header
        (new-array (jstring) "Origin" "Destination" "Walk_distance" "Travel_time"))

(loop for origin in (iterable-to-list *points*)
      do (progn (format t "Processing origin: ~A~%" origin)
                (call-1 *req* set-origin origin)
                (let ((spt (call-1 *router* plan *req*)))
                  (when spt
                    (let ((result (call-1 spt eval *dests*)))
                      (loop for r in (iterable-to-list result)
                            do (call-1 *matrix-csv* add-row
                                       (new-array (jstring)
                                                  (call-1 origin get-string-data "GEOID")
                                                  (thread r
                                                          (call-1 get-individual)
                                                          (call-1 get-string-data "GEOID"))
                                                  (call-1 (call-1 r get-individual)
                                                          get-string-data "GEOID")
                                                  (call-1 (jnew jdouble
                                                                (call-1 r get-walk-distance))
                                                          to-string)
                                                  (call-1 (jnew jinteger (call-1 r get-time))
                                                          to-string)))))))))

(call-1 *matrix-csv* save "traveltime_matrix-fl.csv")
(defconstant end (get-internal-run-time))
(format t "Elapsed time was ~a seconds"
        (coerce (/ (- end start)
                   internal-time-units-per-second)
                'float))
