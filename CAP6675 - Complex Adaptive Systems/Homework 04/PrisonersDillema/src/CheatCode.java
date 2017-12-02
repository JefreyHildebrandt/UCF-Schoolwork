public abstract class CheatCode extends Strategy
{
    public int nextMove()
    {
        int last = opponentLastMove;
        return nextNextMove();
    }

    public abstract int nextNextMove();
}