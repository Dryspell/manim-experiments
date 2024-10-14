# conda activate my-manim-environment
# manim -pql graph/scene.py VGraphVectors
from manim import *
from networkx import complete_graph
from numpy import linalg

graph_layouts = [
    "spring",
    "circular",
    "kamada_kawai",
    "planar",
    "random",
    "shell",
    "spectral",
    "spiral",
]


class VGraphAllAnimations(Scene):
    def construct(self):
        vertices = [1, 2, 3]
        edges = [(1, 2), (2, 3)]
        g = Graph(vertices, edges, layout=graph_layouts[0])

        self.play(Create(g))
        self.wait()
        self.origin_point = g.vertices[0].get_center()

        for i in range(1, len(graph_layouts)):
            self.play(Transform(g, Graph(vertices, edges, layout=graph_layouts[i])))
            self.wait()


class MovingAngle(Scene):
    def construct(self):
        rotation_center = LEFT

        theta_tracker = ValueTracker(110)
        line1 = Line(LEFT, RIGHT)
        line_moving = Line(LEFT, RIGHT)
        line_ref = line_moving.copy()
        line_moving.rotate(
            theta_tracker.get_value() * DEGREES, about_point=rotation_center
        )
        a = Angle(line1, line_moving, radius=0.5, other_angle=False)
        tex = MathTex(r"\theta").move_to(
            Angle(
                line1, line_moving, radius=0.5 + 3 * SMALL_BUFF, other_angle=False
            ).point_from_proportion(0.5)
        )

        self.add(line1, line_moving, a, tex)
        self.wait()

        line_moving.add_updater(
            lambda x: x.become(line_ref.copy()).rotate(
                theta_tracker.get_value() * DEGREES, about_point=rotation_center
            )
        )

        a.add_updater(
            lambda x: x.become(Angle(line1, line_moving, radius=0.5, other_angle=False))
        )
        tex.add_updater(
            lambda x: x.move_to(
                Angle(
                    line1, line_moving, radius=0.5 + 3 * SMALL_BUFF, other_angle=False
                ).point_from_proportion(0.5)
            )
        )

        self.play(theta_tracker.animate.set_value(40))
        self.play(theta_tracker.animate.increment_value(140))
        self.play(tex.animate.set_color(RED), run_time=0.5)
        self.play(theta_tracker.animate.set_value(350))


def matrixFromVectors(v1: Vector, v2: Vector):
    return [
        [1, 1, 1],
        [v1.get_coord(0), v1.get_coord(1), v1.get_coord(2)],
        [
            v2.get_coord(0),
            v2.get_coord(1),
            v2.get_coord(2),
        ],
    ]


class VGraphVectors(VectorScene):
    def construct(self):
        theta_tracker = ValueTracker(0)

        plane = NumberPlane(
            x_range=(-5, 5, 1),
            y_range=(-5, 5, 1),
            x_length=4,
            y_length=4,
        )
        vector = plane.get_vector(
            [-3, -2],
            color=YELLOW,
        )
        rotating_vector = always_redraw(
            lambda: plane.get_vector([2, 2], color=RED).rotate_about_origin(
                theta_tracker.get_value() * DEGREES
            )
        )

        plot_group = Group(plane, vector, rotating_vector)

        vertices = [1, 2, 3]
        edges = [(1, 2), (2, 3)]
        layout = {1: vector.get_end(), 2: [0, 0, 0], 3: rotating_vector.get_end()}
        g = Graph(vertices, edges, layout=layout)

        matr = always_redraw(
            lambda: DecimalMatrix(matrixFromVectors(vector, rotating_vector)).to_edge(
                RIGHT, buff=2
            )
        )
        det = always_redraw(
            lambda: get_det_text(
                matr,
                determinant=linalg.det(matrixFromVectors(vector, rotating_vector)),
                initial_scale_factor=1,
            )
        )
        matrix_group = Group(matr, det)

        g.to_edge(LEFT, buff=2)
        self.add(plot_group, g, matrix_group)

        self.play(theta_tracker.animate.set_value(40), run_time=2)


class CompleteGraphAllAnimations(Scene):
    def construct(self):
        layouts = [
            "spring",
            "circular",
            "kamada_kawai",
            # "planar",
            "random",
            "shell",
            "spectral",
            "spiral",
        ]

        nxGraph = complete_graph(9)
        g = Graph.from_networkx(nxGraph, layout=layouts[0])

        self.play(Create(g))
        self.wait()

        for i in range(1, len(layouts)):
            self.play(Transform(g, Graph.from_networkx(nxGraph, layout=layouts[i])))
            self.wait()
