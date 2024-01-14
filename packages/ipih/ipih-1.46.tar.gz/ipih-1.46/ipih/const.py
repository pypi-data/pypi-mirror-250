class EMAIL:
    SPLITTER: str = "@"
    
class SubscribtionTypes:
    ON_PARAMETERS: int = 1
    ON_RESULT: int = 2
    ON_RESULT_SEQUENTIALLY: int = 4
    
class SERVICE:
    
    EVENT_LISTENER_NAME_PREFIX: str = "_@@EventListener@@_"
    SUPPORT_NAME_PREFIX: str = "_@@Support@@_"