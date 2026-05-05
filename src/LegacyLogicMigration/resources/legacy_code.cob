      *=================================================================
      * PROGRAM: BANK-INTEREST-CALCULATION
      * DESCRIPTION: Debit interest calculation for current accounts
      * AUTHOR: Legacy Banking System
      * DATE: 1987-03-15
      *=================================================================
       IDENTIFICATION DIVISION.
       PROGRAM-ID. CALC-INTEREST.
       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SOURCE-COMPUTER. IBM-370.
       OBJECT-COMPUTER. IBM-370.

       DATA DIVISION.
       WORKING-STORAGE SECTION.

      *-----------------------------------------------------------------
      * MAIN DATA AREA
      *-----------------------------------------------------------------
       01  WS-PARAMETERS.
           05  WS-BALANCE-IN        PIC 9(9)V99 COMP-3.
           05  WS-ANNUAL-RATE       PIC 9(2)V9999 COMP-3.
           05  WS-NUM-DAYS          PIC 9(3) COMP.

       01  WS-CALCULATIONS.
           05  WS-DAILY-INTEREST    PIC 9(9)V99 COMP-3.
           05  WS-TOTAL-INTEREST    PIC 9(9)V99 COMP-3.
           05  WS-FINAL-BALANCE     PIC 9(9)V99 COMP-3.

       01  WS-COUNTER               PIC 9(5) COMP-3 VALUE 0.
       01  WS-ERROR-FLAG            PIC X VALUE 'N'.
           88  ERROR-YES            VALUE 'Y'.
           88  ERROR-NO             VALUE 'N'.

       01  WS-ERROR-MESSAGE         PIC X(50).

       01  WS-MOVEMENTS-TABLE.
           05  WS-MOV-RECORD OCCURS 100 TIMES INDEXED BY WS-IDX.
               10  WS-MOV-ID        PIC 9(5).
               10  WS-MOV-AMOUNT    PIC 9(9)V99 COMP-3.
               10  WS-MOV-TYPE      PIC X(1).
                   88  TYPE-DEBIT   VALUE 'D'.
                   88  TYPE-CREDIT  VALUE 'C'.

      *-----------------------------------------------------------------
      * CONSTANTS
      *-----------------------------------------------------------------
       01  WS-CONSTANTS.
           05  WS-DAYS-PER-YEAR     PIC 9(3) VALUE 365.
           05  WS-DIV-FACTOR        PIC 9(5) VALUE 10000.

       PROCEDURE DIVISION.
      *-----------------------------------------------------------------
      * MAIN SECTION
      *-----------------------------------------------------------------
       MAIN-LOGIC.
           PERFORM INITIALIZATION.
           PERFORM LOAD-TEST-DATA.
           PERFORM CALCULATE-INTEREST.
           PERFORM PRINT-RESULTS.
           PERFORM SAVE-MOVEMENT.
           PERFORM END-PROGRAM.

      *-----------------------------------------------------------------
      * VARIABLE INITIALIZATION
      *-----------------------------------------------------------------
       INITIALIZATION.
           MOVE ZERO TO WS-BALANCE-IN
                        WS-ANNUAL-RATE
                        WS-NUM-DAYS
                        WS-DAILY-INTEREST
                        WS-TOTAL-INTEREST
                        WS-FINAL-BALANCE
                        WS-COUNTER.
           MOVE 'N' TO WS-ERROR-FLAG.
           MOVE SPACES TO WS-ERROR-MESSAGE.

      *-----------------------------------------------------------------
      * LOAD TEST DATA (SIMULATED FILE READ)
      *-----------------------------------------------------------------
       LOAD-TEST-DATA.
      *    FIRST TEST: Standard account
           MOVE 15000.00 TO WS-BALANCE-IN.
           MOVE 0.0350 TO WS-ANNUAL-RATE.
           MOVE 90 TO WS-NUM-DAYS.

      *-----------------------------------------------------------------
      * INTEREST CALCULATION LOGIC
      * Formula: (Principal * Rate * Days) / 365
      *-----------------------------------------------------------------
       CALCULATE-INTEREST.
           IF WS-BALANCE-IN < 0
               MOVE 'Y' TO WS-ERROR-FLAG
               MOVE 'NEGATIVE BALANCE NOT ALLOWED' TO WS-ERROR-MESSAGE
               GO TO END-PROGRAM
           END-IF.

           IF WS-ANNUAL-RATE > 1.0
               MOVE 'Y' TO WS-ERROR-FLAG
               MOVE 'RATE GREATER THAN 100%' TO WS-ERROR-MESSAGE
               GO TO END-PROGRAM
           END-IF.

           IF WS-NUM-DAYS = 0
               MOVE 0 TO WS-TOTAL-INTEREST
               MOVE WS-BALANCE-IN TO WS-FINAL-BALANCE
           ELSE
               COMPUTE WS-TOTAL-INTEREST ROUNDED =
                   (WS-BALANCE-IN * WS-ANNUAL-RATE * WS-NUM-DAYS)
                   / WS-DAYS-PER-YEAR

               ADD WS-TOTAL-INTEREST TO WS-BALANCE-IN
                   GIVING WS-FINAL-BALANCE
           END-IF.

      *-----------------------------------------------------------------
      * PRINT RESULTS
      *-----------------------------------------------------------------
       PRINT-RESULTS.
           DISPLAY '========================================'.
           DISPLAY '    BANK INTEREST CALCULATION REPORT    '.
           DISPLAY '========================================'.
           DISPLAY 'Initial balance: ' WS-BALANCE-IN.
           DISPLAY 'Annual rate:     ' WS-ANNUAL-RATE.
           DISPLAY 'Days:            ' WS-NUM-DAYS.
           DISPLAY '----------------------------------------'.
           DISPLAY 'Net interest:    ' WS-TOTAL-INTEREST.
           DISPLAY 'Final balance:   ' WS-FINAL-BALANCE.
           DISPLAY '========================================'.

      *-----------------------------------------------------------------
      * SAVE MOVEMENT TO TABLE
      *-----------------------------------------------------------------
       SAVE-MOVEMENT.
           ADD 1 TO WS-COUNTER.
           IF WS-COUNTER > 100
               DISPLAY 'ERROR: MOVEMENTS TABLE FULL'
               GO TO END-PROGRAM
           END-IF.

           SET WS-IDX TO WS-COUNTER.
           MOVE WS-COUNTER TO WS-MOV-ID(WS-IDX).
           MOVE WS-TOTAL-INTEREST TO WS-MOV-AMOUNT(WS-IDX).
           MOVE 'C' TO WS-MOV-TYPE(WS-IDX).

           DISPLAY 'Movement saved ID: ' WS-COUNTER.

      *-----------------------------------------------------------------
      * TERMINATION
      *-----------------------------------------------------------------
       END-PROGRAM.
           IF ERROR-YES
               DISPLAY 'ERROR: ' WS-ERROR-MESSAGE
               MOVE 8 TO RETURN-CODE
           ELSE
               DISPLAY 'Processing completed successfully.'
               MOVE 0 TO RETURN-CODE
           END-IF.

           STOP RUN.
